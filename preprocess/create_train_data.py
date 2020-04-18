import os
import re
import pickle
# path_patch = '/Users/haoye.tian/Documents/University/data/quixbugs'
# path_patched = '/Users/haoye.tian/Documents/University/data/quixbugs_wholefile/quicksort'
path_patch_test = '/Users/haoye.tian/Documents/University/data/kui_patches/Patches_test'
path_patch_train = '../data/kui_Patches/Patches_train'

def get_patch_cc2v(patch):
    with open(patch, 'r') as file:
        lines = ''
        p = r"([^\w_])"
        for line in file:
            line = line.strip()
            if line != '':
                if line.startswith('@@') or line.startswith('diff') or line.startswith('index'):
                    continue
                if line.startswith('---'):
                    newline = re.split(pattern=p,string=line[3:].strip())
                    newline = 'mmm ' + ' '.join(newline) + ' <nl> '
                    lines += newline
                elif line.startswith('+++'):
                    newline = re.split(pattern=p,string=line[3:].strip())
                    newline = 'ppp ' + ' '.join(newline) + ' <nl> '
                    lines += newline
                else:
                    newline = re.split(pattern=p, string=line.strip())
                    newline = [x.strip() for x in newline]
                    while '' in newline:
                        newline.remove('')
                    newline = ' '.join(newline) + ' <nl> '
                    lines += newline
        return lines



def get_diff_files(patch,type):
    with open(patch, 'r') as file:
        lines = ''
        flag = True
        # try:
        for line in file:
            line = line.strip()
            if '*/' in line:
                flag = True
                continue
            if flag == False:
                continue
            if line != '':
                if line.startswith('@@') or line.startswith('diff') or line.startswith('index'):
                    continue
                elif '/*' in line:
                    flag = False
                    continue
                elif type == 'buggy':
                    if line.startswith('---'):
                        line = line.split(' ')[1]
                        lines += line.strip() + ' '
                    elif line.startswith('-'):
                        if line[1:].strip().startswith('//'):
                            continue
                        lines += line[1:].strip() + ' '
                    elif line.startswith('+'):
                        # do nothing
                        pass
                    else:
                        lines += line.strip() + ' '
                elif type == 'patched':
                    if line.startswith('+++'):
                        line = line.split(' ')[1]
                        lines += line.strip() + ' '
                    elif line.startswith('+'):
                        if line[1:].strip().startswith('//'):
                            continue
                        lines += line[1:].strip() + ' '
                    elif line.startswith('-'):
                        # do nothing
                        pass
                    else:
                        lines += line.strip() + ' '
        # except Exception:
        #     print(Exception)
        #     return 'Error'
        return lines

def get_whole(path):
    with open(path, 'r') as f:
        lines = ''
        for line in f:
            line = line.strip()
            lines += line + ' '
    return lines

def create_data(path_patch):
    path_patch_list = os.listdir(path_patch)
    path_patch_list = sorted(path_patch_list)
    with open('../data/pre_data_new.txt','w+') as f:
        data = ''
        for file_name in path_patch_list:
            bug_id = file_name
            try:
                buggy = get_diff_files(os.path.join(path_patch, file_name),type='buggy')
                patched = get_diff_files(os.path.join(path_patch, file_name),type='patched')
            except Exception:
                print(Exception)
                continue
            label_temp = '1'
            sample = label_temp + '<ml>'+ bug_id + '<ml>' + buggy + '<ml>' + patched
            data += sample + '\n'
        f.write(data)

def create_data_wholefile(path_patched):
    with open('../data/pre_data_whole.txt','w+') as f:
        data = ''
        for root,dirs,files in os.walk(path_patched):
            for file in files:
                if file == 'QUICKSORT.java':
                    buggy = get_whole('/Users/haoye.tian/Documents/University/data/quixbugs_wholefile/quicksort/QUICKSORT_BUG.java')
                    patched = get_whole(os.path.join(root, file))
                    bug_id = root.split('quicksort/')[1].split('/java_programs')[0]
                    label_temp = '1'
                    sample = label_temp + '<ml>' + bug_id + '<ml>' + buggy + '<ml>' + patched
                    data += sample + '\n'
        f.write(data)

#for future
def create_data_kui2(path_patch_kui):
    with open('../data/pre_data_kui.txt','w+') as f:
        data = ''
        for root,dirs,files in os.walk(path_patch_kui):
            for file in files:
                if file.endswith('txt') or file.endswith('patch'):
                    if file.endswith('src.patch'):
                        bug_id = '_'.join([root.split('/')[-2],root.split('/')[-1], file])
                    else:
                        bug_id = '_'.join([root.split('/')[-1],file])
                    buggy = get_diff_files(os.path.join(root,file),type='buggy')
                    patched = get_diff_files(os.path.join(root, file), type='patched')
                    label_temp = '1'
                    sample = label_temp + '<ml>' + bug_id + '<ml>' + buggy + '<ml>' + patched
                    data += sample + '\n'
                    # with open(root+'/pre_data_kui.txt', 'a+') as f:
                    #     f.write(sample)
        f.write(data)

def create_train_data5(path_patch_kui):
    with open('../data/train_data5.txt','w+') as f:
        data = ''
        for root,dirs,files in os.walk(path_patch_kui):
            if files == ['.DS_Store']:
                continue
            # files = sorted(files,key=lambda x:int(x.split('-')[1].split('.')[0]))
            for file in files:
                # if root.startswith('../data/kui_Patches/Patches_train/Bears'):
                #     pass
                if file.endswith('txt') or file.endswith('patch'):
                    if file.endswith('.patch'):
                        bug_id = '_'.join([root.split('/')[-2],root.split('/')[-1], file])
                    else:
                        bug_id = '_'.join([root.split('/')[-1],file])
                    try:
                        # if bug_id.endswith('Bears-114.txt'):
                            # pass
                        buggy = get_diff_files(os.path.join(root,file),type='buggy')
                        patched = get_diff_files(os.path.join(root, file), type='patched')
                    except Exception as e:
                        print(e)
                        continue
                    label_temp = '1'
                    sample = label_temp + '<ml>' + bug_id + '<ml>' + buggy + '<ml>' + patched
                    data += sample + '\n'
                    # with open(root+'/pre_data_kui.txt', 'a+') as f:
                    #     f.write(sample)
        f.write(data)

def create_train_data5_frag(path_patch_kui):
    with open('../data/train_data5_frag.txt','w+') as f:
        data = ''
        for root,dirs,files in os.walk(path_patch_kui):
            if files == ['.DS_Store']:
                continue
            # files = sorted(files,key=lambda x:int(x.split('-')[1].split('.')[0]))
            for file in files:
                # if root.startswith('../data/kui_Patches/Patches_train/Bears'):
                #     pass
                if file.endswith('txt') or file.endswith('patch'):
                    if file.endswith('.patch'):
                        bug_id = '_'.join([root.split('/')[-2],root.split('/')[-1], file])
                    else:
                        bug_id = '_'.join([root.split('/')[-1],file])
                    try:
                        # if bug_id.endswith('Bears-114.txt'):
                            # pass
                        buggy = get_diff_files(os.path.join(root,file),type='buggy')
                        patched = get_diff_files(os.path.join(root, file), type='patched')
                    except Exception as e:
                        print(e)
                        continue
                    label_temp = '1'
                    sample = label_temp + '<ml>' + bug_id + '<ml>' + buggy + '<ml>' + patched
                    data += sample + '\n'
                    # with open(root+'/pre_data_kui.txt', 'a+') as f:
                    #     f.write(sample)
        f.write(data)

def create_train_data5_for_cc2v(path_patch_kui):
    with open('../data/train_data5_for_cc2v.txt','w+') as f:
        data = ''
        for root,dirs,files in os.walk(path_patch_kui):
            if files == ['.DS_Store']:
                continue
            # files = sorted(files,key=lambda x:int(x.split('-')[1].split('.')[0]))
            for file in files:
                if file.endswith('txt') or file.endswith('patch'):
                    if file.endswith('.patch'):
                        bug_id = '_'.join([root.split('/')[-2],root.split('/')[-1], file])
                    else:
                        bug_id = '_'.join([root.split('/')[-1],file])
                    try:
                        patch_cc2v = get_patch_cc2v(os.path.join(root, file))
                    except Exception as e:
                        print(e)
                        continue
                    label_temp = '1'
                    sample = label_temp + '<ml>' + bug_id + '<ml>' + patch_cc2v
                    data += sample + '\n'
        f.write(data)

if __name__ == '__main__':
    # create_data(path_patch)
    # create_data_wholefile(path_patched)

    create_train_data5(path_patch_train)
    create_train_data5_frag(path_patch_train)
    create_train_data5_for_cc2v(path_patch_train)