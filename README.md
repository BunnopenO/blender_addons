## export_fbx_bin
ビルトインのFBXエクスポートアドオンから修正。
UE4にてArmatureオブジェクトがルートボーンとして読み込まれる問題を解消します。

***

This based on built-in FBX export addon.
It makes armature object to be not imported as root bone in UE4. (Extra root bone problem)

## rigify_to_ue4
Rigifyによって生成されたrigをUE4Mannequinのスケルトンに近いものに変換します。
* 手足に複数のツイストボーンを持ちます。
* Rigifyの「Tweak」ボーンの動作を一部サポートします。

#### 使用法
* Rigifyの使用手順に従い「Generate」を行います。また生成されたアーマチュア「rig」を選択した状態にします。
* 本スクリプトをTextEditウィンドウで開き、「Run Script」を実行します。
* 実行することで元のDeformボーンは非Deformボーンとなり、レイヤー「23」に新たなDeformボーン(FCP-)が生成されます。

#### 注意事項
* 「metarig」を編集する場合、複製されたボーンの名前は「~~.001」となりますが、必ず「.」(ドット)以降を削除し、新たな名前を設定して下さい。
* 特定のボーンの名前は変更しないで下さい。(upper_arm、forearm、hand、thigh、shin、foot)

##### 注意！　このスクリプトは開発中のものです。

***

This script converts a rig into similar bone structure of UE4 Mannequin's skeleton.
* Converted rig has some twist bones on its limbs.
* Partial support of Rigify's tweak bones.

#### Usages
* Generate rigify.
* Select generated armature.
* Run script with TextEdit window. Script generates 'FCP-' bones in armature layer[23]. Simultaneously, other bones will be set as non deform bone.

#### Precautions
* Don't make duplicated name bone (e.g. '.001') in metarig.
* Don't change specific bones' name. (upper_arm, forearm, hand, thigh, shin and foot)

##### Warning! This script is under trial.

## catenary.py
頂点編集において懸垂線（カテナリー）を作成します。

#### 使用法
Editモードで２点を選択した後、「Create Catenary」で適用します。
分割数と垂らす度合い、上下逆転のオプションがあります。

#### 既知の問題
* ２点が垂直な直線状に位置している場合、分割のみ行われてObjectモードに戻ります。Undoは機能します。
