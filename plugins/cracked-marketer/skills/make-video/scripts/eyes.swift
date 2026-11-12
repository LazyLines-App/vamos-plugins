// eyes.swift <image>...: how open each eye is in each frame, from Apple Vision's face landmarks (macOS).
// Prints one JSON line an image: gapL/gapR (lid gap over eye width) and darkL/darkR (the share of the eye box
// darker than the cheek below it: the iris and pupil, gone when the lids close). checklib.eyes() reads these
// against the same take's own open eye, so faces and light don't matter.
import AppKit
import Foundation
import Vision

func grey(_ cg: CGImage) -> ([UInt8], Int, Int) {
    let w = cg.width, h = cg.height
    var buf = [UInt8](repeating: 0, count: w * h)
    let ctx = CGContext(data: &buf, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w,
                        space: CGColorSpaceCreateDeviceGray(), bitmapInfo: 0)!
    ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
    return (buf, w, h)
}

func measure(_ region: VNFaceLandmarkRegion2D?, _ g: [UInt8], _ W: Int, _ H: Int) -> (Double, Double)? {
    guard let r = region, r.pointCount >= 6 else { return nil }
    let pts = r.pointsInImage(imageSize: CGSize(width: W, height: H))
    let xs = pts.map { Double($0.x) }, ys = pts.map { Double(H) - Double($0.y) }
    let x0 = Int(xs.min()!), x1 = Int(xs.max()!), w = Double(x1 - x0)
    guard w >= 8 else { return nil }
    let yc = (ys.min()! + ys.max()!) / 2
    var cheek: [Int] = []
    for y in Int(yc + w * 0.6)..<Int(yc + w * 0.9) where y >= 0 && y < H {
        for x in x0..<x1 where x >= 0 && x < W { cheek.append(Int(g[y * W + x])) }
    }
    cheek.sort()
    let skin = Double(cheek.isEmpty ? 128 : cheek[cheek.count / 2])
    var dark = 0, n = 0
    for y in Int(yc - w * 0.25)..<Int(yc + w * 0.25) where y >= 0 && y < H {
        for x in x0..<x1 where x >= 0 && x < W {
            n += 1
            if Double(g[y * W + x]) < skin * 0.55 { dark += 1 }
        }
    }
    return ((ys.max()! - ys.min()!) / w, Double(dark) / Double(max(n, 1)))
}

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("{\"image\":\"\(path)\",\"face\":false}"); continue
    }
    let req = VNDetectFaceLandmarksRequest()
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    let (g, W, H) = grey(cg)
    guard let f = (req.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width }),
          let l = measure(f.landmarks?.leftEye, g, W, H), let r = measure(f.landmarks?.rightEye, g, W, H) else {
        print("{\"image\":\"\(path)\",\"face\":false}"); continue
    }
    print(String(format: "{\"image\":\"%@\",\"face\":true,\"gapL\":%.4f,\"gapR\":%.4f,\"darkL\":%.4f,\"darkR\":%.4f}",
                 path, l.0, r.0, l.1, r.1))
}
