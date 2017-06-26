# -*- mode: python -*-

block_cipher = None


def res_dir(source, target, res_datas=None):
    """
    Prefix is left out when translated to spec-file.
    """
    if res_datas is None:
        res_datas = []
    import os
    for file in os.listdir(source):
        if os.path.isdir(file):
            res_datas.extend(res_dir(source+file+"/",target+file+"/",res_datas))
        else:
            res_datas.append((target + file, source + file, 'DATA'))
    return res_datas



a = Analysis(['src/easypie.py'],
             pathex=['/home/axxessio/workspace/Work/IT4Kids/easypie'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += res_dir('src/gui/res/','gui/res/')
a.datas += [("gui/style.css","src/gui/style.css","DATA")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Easypie',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='src/gui/res/icon.png')
