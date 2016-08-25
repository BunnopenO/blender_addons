## export_fbx_bin
ビルトインのFBXエクスポートアドオンから修正。
UE4にてArmatureオブジェクトがルートボーンとして読み込まれる問題を解消します。

## rigify_to_ue4
Rigifyによって生成されたrigをUE4Mannequinのスケルトンに近いものに変換します。

#### 使用法
* Rigifyの使用手順に従い「Generate」を行います。また生成されたアーマチュア「rig」を選択した状態にします。
* 本スクリプトをTextEditウィンドウで開き、「Run Script」を実行します。
* 実行することで元のDeformボーンは非Deformボーンとなり、レイヤー「」に新たなDeformボーンが生成されます。新たなボーンに対してWeight設定を行います。(「Set Parent To」→「With Automatic Weights」等)

* Generate rigify.
* Select generated armature.
* Run script. Script generates 'FCP-' bones in armature layer[23]. Simultaneously, other bones will be set as non deform bone.

#### 注意事項
「metarig」を編集する場合、複製されたボーンの名前は「~~.001」となりますが、必ず「.」(ドット)以降を削除し、新たな名前を設定して下さい。
特定のボーンの名前は変更しないで下さい。(upper_arm、forearm、hand、thigh、shin、foot)

Don't make duplicated name bone (e.g. '.001') in metarig.
Don't change specific bones' name. (upper_arm, forearm, hand, thigh, shin and foot)

注意！　このスクリプトは開発中のものです。
Warning! This script is under trial.
