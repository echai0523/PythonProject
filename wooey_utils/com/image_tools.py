# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2021-12-29 12:28
Short Description:

Change History:

通用的语意分割格式，改成扁平格式


'''
import json

# json_str = '''{"auditId":"preview-Le1kMpojnyWnoQ0jUjyKC.video-track_record.audit","instances":[{"id":"9d7d9a66-8c21-4b8e-b13a-ced11c762d9c","category":"公交车","number":1,"children":[{"id":"a83f46c9-e6dd-4a9f-9242-0ecabbfb67a0","name":"车身","number":1,"cameras":[{"camera":"default","frames":[{"frameIndex":0,"isKeyFrame":true,"shapeType":"rectangle","shape":{"x":198,"y":80,"width":141,"height":76,"rotation":0,"points":[{"x":198,"y":80},{"x":339,"y":80},{"x":339,"y":156},{"x":198,"y":156}]},"order":11,"isOCR":false}]}]},{"id":"59f44122-1624-48db-bc01-7b3f8e8a6d13","name":"车身","number":2,"cameras":[{"camera":"default","frames":[{"frameIndex":0,"isKeyFrame":true,"shapeType":"rectangle","shape":{"x":405,"y":99,"width":161,"height":79,"rotation":0,"points":[{"x":405,"y":99},{"x":566,"y":99},{"x":566,"y":178},{"x":405,"y":178}]},"order":12,"isOCR":false}]}]},{"id":"25a9ff47-fd73-4381-aa85-9692adc77979","name":"车头","number":1,"cameras":[{"camera":"default","frames":[{"frameIndex":0,"isKeyFrame":true,"shapeType":"rectangle","shape":{"x":-129.08295298192388,"y":311.0849048440091,"width":143.68427310459776,"height":169.80868639634286,"rotation":0,"points":[{"x":-129.08295298192388,"y":311.0849048440091},{"x":14.601320122673883,"y":311.0849048440091},{"x":14.601320122673883,"y":480.89359124035195},{"x":-129.08295298192388,"y":480.89359124035195}]},"order":18,"isOCR":false}]}]}]},{"id":"31bc310f-fcdd-4319-9db0-83ece60502a2","category":"公交车","number":2,"children":[{"id":"62848ddd-604a-4804-9f98-d06cb0e1cf20","name":"车身","number":1,"cameras":[{"camera":"default","frames":[{"frameIndex":0,"isKeyFrame":true,"shapeType":"rectangle","shape":{"x":628,"y":96,"width":129,"height":102,"rotation":0,"points":[{"x":628,"y":96},{"x":757,"y":96},{"x":757,"y":198},{"x":628,"y":198}]},"order":13,"isOCR":false}]}]}]},{"id":"64eb78ca-fd49-48e0-a347-e537c98de6a9","category":"遮挡物","number":1,"children":[{"id":"c090fad3-8d3f-46bd-94de-df416216fc7c","name":"遮挡部件","number":1,"cameras":[{"camera":"default","frames":[{"frameIndex":0,"isKeyFrame":true,"shapeType":"polygon","shape":{"points":[{"x":132,"y":324},{"x":133,"y":313},{"x":138,"y":301},{"x":149,"y":288},{"x":159,"y":275},{"x":166,"y":264},{"x":172,"y":253},{"x":174,"y":242},{"x":182.85601404741,"y":237.1694468832309},{"x":301,"y":273},{"x":313,"y":275},{"x":323,"y":287},{"x":325,"y":302},{"x":308,"y":323},{"x":269,"y":362},{"x":250,"y":379},{"x":231,"y":393},{"x":208,"y":406},{"x":188,"y":416},{"x":174,"y":418},{"x":162,"y":417},{"x":153,"y":406},{"x":145,"y":392},{"x":138,"y":381},{"x":133,"y":365},{"x":132,"y":353}]},"order":14,"isOCR":false}]}]},{"id":"e4026d6a-7664-43cd-b51c-d6630a34bdf4","name":"遮挡部件","number":2,"cameras":[{"camera":"default","frames":[{"frameIndex":0,"isKeyFrame":true,"shapeType":"polygon","shape":{"points":[{"x":425,"y":307},{"x":470,"y":307},{"x":501,"y":309},{"x":520,"y":310},{"x":542,"y":313},{"x":561,"y":316},{"x":583,"y":320},{"x":607,"y":328},{"x":608,"y":339},{"x":596,"y":351},{"x":583,"y":361},{"x":570,"y":372},{"x":559,"y":381},{"x":529,"y":403},{"x":508,"y":419},{"x":484,"y":436},{"x":459,"y":452},{"x":445,"y":459},{"x":434,"y":462},{"x":429,"y":451},{"x":425,"y":437},{"x":422,"y":421},{"x":418,"y":404},{"x":414,"y":384},{"x":414,"y":368},{"x":420,"y":356},{"x":427,"y":344},{"x":433,"y":331},{"x":438,"y":319},{"x":441,"y":308}]},"order":15,"isOCR":false}]}]}]},{"id":"452dc571-9952-4a81-9206-5fd160ee1a95","category":"小轿车","number":1,"children":[{"id":"badc77b7-b3fb-4ba6-8c14-f86a034c8076","name":"default","number":1,"cameras":[{"camera":"default","frames":[{"frameIndex":0,"isKeyFrame":true,"shapeType":"polygon","shape":{"points":[{"x":53,"y":119},{"x":66,"y":125},{"x":74,"y":136},{"x":74,"y":147},{"x":69,"y":158},{"x":62,"y":170},{"x":50,"y":179},{"x":37,"y":182},{"x":28,"y":170},{"x":29,"y":158},{"x":32,"y":146},{"x":36,"y":135},{"x":41,"y":123},{"x":52,"y":119}]},"order":16,"isOCR":false}]}]}]},{"id":"0f790c19-1368-4224-bc78-f8f360ec922e","category":"小轿车","number":2,"children":[{"id":"0db0c883-e691-4dcd-a0e7-0049beac85d1","name":"default","number":1,"cameras":[{"camera":"default","frames":[{"frameIndex":0,"isKeyFrame":true,"shapeType":"rectangle","shape":{"x":64,"y":202,"width":10,"height":107,"rotation":0,"points":[{"x":64,"y":202},{"x":74,"y":202},{"x":74,"y":309},{"x":64,"y":309}]},"order":17,"isOCR":false}]}]}]}],"frames":[],"statistics":"https://oss-prd.appen.com.cn:9001/tool-prod/preview-Le1kMpojnyWnoQ0jUjyKC/preview-Le1kMpojnyWnoQ0jUjyKC.video-track_task.video-track_record.result.stat.json"}
# '''

# json_dict = json.loads(json_str)

def flat_common_image_json(json_dict,is_single_frame=False):
    instances_list = []
    for ins in json_dict["instances"]:

        ins_template = {
            "id": ins["id"],
            "category": ins["category"],
            "category_number": ins["number"],
        }
        for item in ins["children"]:
            new_item = {
                **ins_template,
                "child_id":item["id"],
                "child_name":item["name"],
                "child_number":item["number"],
                # "frames":item["cameras"][0]["frames"]
            }
            if is_single_frame == False:
                # print("frames")
                new_item["frames"] = item["cameras"][0]["frames"]
            else:
                # print("frame")
                new_item["frame"] =  item["cameras"][0]["frames"][0]

            instances_list.append(new_item)
    print(json.dumps(instances_list, ensure_ascii=False))
    return instances_list



# flat_common_image_json(json_dict,is_single_frame=True)


