import os
import json
import fire
from glob import glob
from tqdm import tqdm

from summertime.evaluation import Rouge, RougeWe, BertScore, Bleu, Meteor
from utils.MoverScore import MoverScore

METRICS = [Rouge(), RougeWe(), BertScore(), Bleu(), Meteor()]



def load_split_data(fpath):
    """
        Load split data: train, test, dev --> List()
        Data structure:
            {id:(str) , summary:(str), source:(str),}
    """
    tmp = []
    with open(fpath, 'r') as r:
        for line in r:
            tmp.append(json.loads(line))
    return tmp

def run_evaluation(model_summaries, tgt, BlockList=[]):
    """
        Run all metrics for summarization results
    """

    result = dict()
    print("evaluating...")
    for metric in METRICS:
        print(f"evaluating {metric.metric_name}...")
        if metric.metric_name in BlockList:
            continue
        results = metric.evaluate(model_summaries, tgt)
        print(f"{metric.metric_name} results: {results}")
        result[metric.metric_name] = results
    
    if "moverscore" not in BlockList:
        result['MoverScore'] = MoverScore(model_summaries, tgt)
        print(f"MoverScore results: {result['MoverScore']}")
    return result

# run evaluation by summertime
def get_tgt_pred(temp_data):
    ids = []
    tgt_list = []
    pred_list = []
    print("loading data...")
    for ins in tqdm(temp_data):
        if "id" in ins.keys():
            ids.append(ins['id'])
        else:
            ids = []
        if "target" in ins.keys():
            tgt_list.append(ins['target'])
            pred_list.append(ins['prediction'])
        elif "summary" in ins.keys():
            tgt_list.append(ins['summary'])
            pred_list.append(ins['prediction'])
        elif "ModelPrediction" in ins.keys():
            tgt_list.append(ins["GroundTruth"])
            pred_list.append(ins["ModelPrediction"])
    return {"ids":ids, "tgt":tgt_list, "pred":pred_list}

def run_eval(fpath):
    data_name = os.path.basename(fpath).split(".")[0]
    eval_data = get_tgt_pred(load_split_data(fpath))
    return {data_name: run_evaluation(eval_data['pred'], eval_data['tgt'])}  

if __name__ == "__main__":
    fire.Fire(run_eval)

    