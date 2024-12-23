# script.ps1

# 获取当前脚本所在目录
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path $scriptPath

# 定义虚拟环境路径
$venvPath = "$scriptDir\venv\Scripts\Activate.ps1"

# 激活虚拟环境
& $venvPath

# 指定要删除的文件夹路径
$folderPath = ".\data"

# 检查文件夹是否存在
if (Test-Path $folderPath) {
    try {
        # 删除文件夹及其内容
        Remove-Item -Path $folderPath -Recurse -Force
        Write-Output "文件夹已成功删除：$folderPath"
    } catch {
        Write-Error "删除文件夹时出错：$($_.Exception.Message)"
    }
} else {
    Write-Output "文件夹不存在：$folderPath"
}

# 在虚拟环境中运行命令，例如安装包
# pip install requests

# 你的其他命令
python main.py
