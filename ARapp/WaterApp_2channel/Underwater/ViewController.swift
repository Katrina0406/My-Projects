//
//  ViewController.swift
//  Underwater
//
//  Created by 胡雨乔 on 3/8/22.
//  Copyright © 2022 Apple. All rights reserved.
//

import UIKit
import SceneKit
import ARKit
import Foundation
import RealityKit


class ViewController: UIViewController {
    @IBOutlet weak var sceneView2: UnderwaterView!
    @IBOutlet weak var sceneView1: UnderwaterView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    // UPDATE EVERY FRAME:
    func renderer(_ renderer: SCNSceneRenderer, updateAtTime time: TimeInterval) {
        DispatchQueue.main.async {
            self.updateFrame()
        }
    }
    
    func updateFrame() {
        
        // Clone pointOfView for Second View
        var pointOfView : Transform = (sceneView1.cameraTransform)
        
        // Determine Adjusted Position for Right Eye
        let orientation : simd_float4 = pointOfView.rotation.vector
        let orientationQuaternion : GLKQuaternion = GLKQuaternionMake(orientation.x, orientation.y, orientation.z, orientation.w)
        let eyePos : GLKVector3 = GLKVector3Make(1.0, 0.0, 0.0)
        let rotatedEyePos : GLKVector3 = GLKQuaternionRotateVector3(orientationQuaternion, eyePos)
        let rotatedEyePosSCNV : SCNVector3 = SCNVector3Make(rotatedEyePos.x, rotatedEyePos.y, rotatedEyePos.z)
        
        let mag : Float = 0.066 // This is the value for the distance between two pupils (in metres). The Interpupilary Distance (IPD).

        pointOfView.translation.x += rotatedEyePosSCNV.x * mag
        pointOfView.translation.y += rotatedEyePosSCNV.y * mag
        pointOfView.translation.z += rotatedEyePosSCNV.z * mag
        
        // Set PointOfView for SecondView

        sceneView2.camera?.position = pointOfView.translation
        
    }
}
