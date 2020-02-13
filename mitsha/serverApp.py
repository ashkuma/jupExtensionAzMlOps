from flask import Flask, redirect

app = Flask(__name__)

@app.route('/openLocal/<git_url>', methods=['GET'])
def openLocal(git_url):
    import subprocess as sb 
    import os
    repo_name = git_url.split('.')[-1]
    CUR_DIR = os.getcwd()
    os.chdir("C:\\Users\\mitsha\\")
    try:
        os.chdir(repo_name)
        print('Repo was already cloned.')
        p1 = sb.Popen('jupyter notebook',shell=True)
        os.chdir(CUR_DIR)
        return '<h1>Opening the Jupyter Notebook</h1>'
    except:
        print('Repo is not cloned.')
        p1 = sb.Popen('git clone https://github.com/{repo_name}.git'.format(repo_name=git_url.replace('.','/')), shell=True)
        p1.wait()
        os.chdir(repo_name)
        p1 = sb.Popen('jupyter notebook',shell=True)
        os.chdir(CUR_DIR)
        return '<h1>Opening the Jupyter Notebook</h1>'

if __name__ == '__main__':
    port = 8000
    app.run(host='0.0.0.0',port=port,debug=True)
