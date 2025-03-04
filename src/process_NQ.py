import os
import json
import argparse

from tqdm import tqdm

def load_json(fname, mode="r", encoding="utf8"):
    if "b" in mode:
        encoding = None
    with open(fname, mode=mode, encoding=encoding) as f:
        return json.load(f)
    
def load_data(split, args):
    data_file_name = 'Data/{}/label_map/{}_{}.json'.format(args.dataset_type,args.dataset_type,split)
    print('Loading data from:',data_file_name)
    data_dict = load_json(data_file_name)
    return data_dict

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_type', type=str, help="LC-QuAD2.0")
    args = parser.parse_args()
    return args

def prepare_dataloader(args,split):
    assert split in ['train','test','dev','train_sample','dev_sample','test_sample']

    data = load_data(split, args)
    print(f'Origin {split} dataset len: {len(data)}')
    assert type(data)==list
    if 'train' in split or 'dev' in split:
        # for train and dev, filter the examples without sexpr
        examples = []
        for x in data:
            if x['s_expr'].lower()!="null":
                examples.append(x)                
    else:
        examples = [x for x in data]
    print(f'Real {split} dataset len: {len(examples)}')

    json_data=[]
    instruction='Tạo truy vấn Logical Form để lấy thông tin tương ứng với câu hỏi đã cho. \n'
    for cnt, item in tqdm(enumerate(examples)):
        question=item['question_vi']
        input = 'Question: { '+question+' }'       
        output = item['nor_s_expr']
        json_data.append({"instruction":instruction,"input":input,"output":output,"history":[]})
               
    
    output_dir = 'LLMs/Data/{}_Wikidata_NQ_{}/examples.json'.format(args.dataset_type, split)

    if not os.path.exists(os.path.dirname(output_dir)):
        os.mkdir(os.path.dirname(output_dir))   

    with open(output_dir, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False)  
    

if __name__=='__main__':
    
    args = _parse_args()
    print(args)
    prepare_dataloader(args,'train')
    prepare_dataloader(args, 'test')
    print('Finished')

