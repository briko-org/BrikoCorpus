from langdetect import detect
from re import match
import string, argparse
def RemoveBracket(full_content):
    '''
        句子开头为"【"时删除【】之间的内容
    '''
    temp_full = []  
    for i, content in enumerate(full_content):
        temp_content = []
        for line in content:
            try:
                if line[0] == "【":
                    line = line[line.index("】") + 1:] 
                temp_content.append(line)
            except:
                print(f'Error when removing 【】 in line: {line}')
        temp_full.append(temp_content)

    return temp_full

def CombineLines(full_content):
    '''
        每段文字中，行尾判断为句终时，可衔接下句。      
    '''
    temp_full = []
    for i, content in enumerate(full_content):
        temp_content = []
        new_line = ""
        can_combine = False
        for line in content:
            if can_combine:
                new_line += line
            else:
                if not new_line == '':
                    temp_content.append(new_line)
                new_line = line
            try:
                can_combine = (line[-1] in "。！？”）：」")
            except:
                can_combine = False
        if not new_line == '':
            temp_content.append(new_line)
        
        temp_full.append(CutSentence(temp_content))
    return temp_full

def CutSentence(content):
    '''
        删除每行文字中前后无法判断是否完整的句子
    '''
    prev_line = ""
    comp_line = False
    temp_content = []
    for line in content:
        
        if prev_line == "":
            comp_line = False
        else:
            comp_line = CompleteSentence(prev_line)
        rm_line = ''
        prev_line = line
        while not CompleteSentence(line):
            rm_line = line[-1] + rm_line
            line = line[:-1]           
            if line == '':
                break
        if not comp_line:
            if not line == '':
                line = RemoveStart(line)
        if not line == '':
            temp_content.append(line)
    return temp_content 

def CompleteSentence(line):
    '''
        判断句尾是否为句终
    '''
    for symb in (["。","。）","？","？）","！”","！）","。」","！」", "？」"]):
        if line.endswith(symb):
            return True
    return False

def RemoveStart(line):
    '''
        删除改行在第一个句终前的所有内容
    '''
    try:
        reach_end = False
        rm_line = ''
        while not reach_end:
            if line[0] in "。！？":
                reach_end = True
                if line[1] in "）”":
                    rm_line += line[0]
                    line = line[1:]
            rm_line += line[0]        
            line = line[1:]

            if line == '':
                break
        return line
    except Exception as ex:
        #print(ex, line)
        return ''

def RemoveSpace(line):
    '''
        删除句子中的空格，除非空格两侧都为英文/数字
    '''
    new_line = ''
    for i, char in enumerate(line):
        if not char == ' ':
            new_line += char
        else:
            if i > 0 and i < (len(line) -1):
                if line[i-1] in string.ascii_letters and line[i+1] in string.ascii_letters:
                    new_line += char
    return new_line

def ApplyFilters(full_content):
    final_lines = []
    web_exc = ["http:", "https:", ".com", ".net", ".cn", "www."]
    for i, content in enumerate(full_content):
        if not content == []:
            for line in content:
                #删除小于20token的句子
                if len(line) >= 20:
                    #删除非中文的句子
                    if 'zh' in detect(line):
                        #删除带email的句子
                        if not match('[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}',line):
                            #删除带网址的句子
                            is_web = False
                            for exc in web_exc:
                                if exc in line:
                                    is_web = True
                                    break
                            if not is_web:
                                line = RemoveSpace(line)
                                #remain_char += len(line)
                                final_lines.append(line)
    return final_lines

def RemoveDuplicated(full_content):
    '''
        排序，并删除重复语料
    '''
    full_content.sort()
    out_content = []
    pre_line = " "
    for li in full_content:        
        if not (li==pre_line): 
            out_content.append(li)
        pre_line = li           
    return out_content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apply filters to the extracted raw content.')
    
    parser.add_argument(
        '-raw_path',
        dest='raw_path',
        default='RawContent.txt',
        type=str,
        help='Path to the raw content.',
    )
    parser.add_argument(
        '-corpus_path',
        dest='corpus_path',
        default='FinalContent.txt',
        type=str,
        help='Path to the BrikoCorpus.',
    )
    args = parser.parse_args()
    raw_content = []
    
    with open(args.raw_path,'r') as rawContent:
        raw_content = rawContent.read().splitlines()
    
    filtered_content = RemoveBracket(raw_content)
   
    filtered_content = CombineLines(filtered_content)
    
    filtered_content = ApplyFilters(filtered_content)
    
    filtered_content = RemoveDuplicated(filtered_content)
    
    with open(args.corpus_path, 'w') as finalContent:
        for line in filtered_content:
            finalContent.write(line+'\n')