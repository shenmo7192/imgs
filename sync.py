#!/usr/bin/env python3
import os
import sys
import subprocess

program_path = os.path.split(os.path.realpath(__file__))[0]
repo_name = "imgs"  # 目标仓库名称

# 配置仓库URL
github_repo_url = "https://github.com/shenmo7192/imgs.git"
atomgit_url_template = "https://{username}:{password}@atomgit.com/shenmo7192/imgs.git"

def validate_credentials():
    if len(sys.argv) != 3:
        print("请提供AtomGit的用户名和密码作为参数")
        print("使用示例: ./sync_script.py username password")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

def clone_and_sync(username, password):
    clone_dir = os.path.join(program_path, "git-clone")
    os.makedirs(clone_dir, exist_ok=True)
    
    # 克隆GitHub仓库（bare方式）
    clone_cmd = f"git clone --bare {github_repo_url} {repo_name}.git"
    subprocess.run(clone_cmd, shell=True, cwd=clone_dir, check=True)
    
    repo_path = os.path.join(clone_dir, f"{repo_name}.git")
    
    try:
        # 设置AtomGit远程地址
        atomgit_url = atomgit_url_template.format(username=username, password=password)
        remote_cmd = f"git remote set-url --push origin {atomgit_url}"
        subprocess.run(remote_cmd, shell=True, cwd=repo_path, check=True)
        
        # 执行镜像推送
        push_cmd = "git push --mirror"
        subprocess.run(push_cmd, shell=True, cwd=repo_path, check=True)
        
        print(f"\n✅ 同步成功！仓库已更新到AtomGit")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 同步失败：{str(e)}")
        sys.exit(1)
    finally:
        # 清理临时文件
        subprocess.run(f"rm -rf {repo_path}", shell=True, check=True)

if __name__ == "__main__":
    username, password = validate_credentials()
    clone_and_sync(username, password)
