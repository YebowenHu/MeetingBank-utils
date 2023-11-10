from datasets import load_dataset
meetingbank = load_dataset("huuuyeah/meetingbank")

# load splits
train_data = meetingbank['train']
test_data = meetingbank['test']
val_data = meetingbank['validation']

# easy generator
def generator(data_split):
  for instance in data_split:
    yiled instance['id'], instance['summary'], instance['transcript']
