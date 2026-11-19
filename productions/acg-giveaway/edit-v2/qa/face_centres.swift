import Foundation
import Vision
import AppKit
let dir=CommandLine.arguments[1]
let files=try FileManager.default.contentsOfDirectory(atPath:dir).filter{$0.hasSuffix(".jpg")}.sorted()
var rows:[[String:Any]]=[]
for f in files {
 let url=URL(fileURLWithPath:dir).appendingPathComponent(f)
 let req=VNDetectFaceRectanglesRequest()
 try VNImageRequestHandler(url:url).perform([req])
 let faces=(req.results ?? []).sorted{$0.boundingBox.width*$0.boundingBox.height > $1.boundingBox.width*$1.boundingBox.height}
 let vals=faces.map{["x":$0.boundingBox.midX,"y":$0.boundingBox.midY,"w":$0.boundingBox.width,"h":$0.boundingBox.height]}
 rows.append(["file":f,"faces":vals])
}
let data=try JSONSerialization.data(withJSONObject:rows,options:[.prettyPrinted,.sortedKeys])
print(String(data:data,encoding:.utf8)!)
