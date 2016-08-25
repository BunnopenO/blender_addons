## export_fbx_bin
ビルトインのFBXエクスポートアドオンから修正。
UE4にてArmatureオブジェクトがルートボーンとして読み込まれる問題を解消します。

## rigify_to_ue4
Rigifyによって生成されたrigをUE4Mannequinのスケルトンに近いものに変換します。

#### 使用法
* Rigifyの使用手順に従い「Generate」を行います。また生成されたアーマチュア「rig」を選択した状態にします。
* 本スクリプトをTextEditウィンドウで開き、「Run Script」を実行します。
* 実行することで元のDeformボーンは非Deformボーンとなり、レイヤー「」に新たなDeformボーンが生成されます。新たなボーンに対してWeight設定を行います。(「Set Parent To」→「With Automatic Weights」等)
