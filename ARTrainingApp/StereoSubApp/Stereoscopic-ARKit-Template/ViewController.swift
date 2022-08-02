//
//  ViewController.swift
//  Stereoscopic-ARKit-Template
//
//  Created by Hanley Weng on 1/7/17.
//  Copyright © 2017 CompanyName. All rights reserved.
//

import UIKit
import SceneKit
import ARKit
import Foundation
import RealityKit

class ViewController: UIViewController, ARSCNViewDelegate {
    
    @IBOutlet weak var sceneView: ARSCNView!
    
    @IBOutlet weak var sceneView2: ARSCNView!
    
    var originalSource: Any? = nil
    var setBlack: Bool = false
    var counts = 0
    var detected = false

//    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
////    if originalSource == nil {
////    originalSource = sceneView.scene.background.contents
////
////    sceneView.scene.background.contents = UIColor.black
////
////    } else {
////    sceneView.scene.background.contents = originalSource
////
////    }
//        if originalSource == nil {
//            originalSource = sceneView.scene.background.contents}
//
//        if !setBlack{
//            sceneView.scene.background.contents = originalSource
//
//        } else {
//            sceneView.scene.background.contents = UIColor.black
//        }
//        setBlack = !setBlack
//
//    }
//
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Set the view's delegate
        sceneView.delegate = self
        
        // Show statistics such as fps and timing information
        sceneView.showsStatistics = true
        
        sceneView.debugOptions = [SCNDebugOptions.showWireframe, SCNDebugOptions.showFeaturePoints, SCNDebugOptions.showCreases]
        let scene = SCNScene(named: "cropped/mesh_model.obj")!
        
        // Set the scene to the view
        sceneView.scene = scene
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        setUpSceneView()
        addTapGestureToSceneView()
        
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        
        // Pause the view's session
        sceneView.session.pause()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Release any cached data, images, etc that aren't in use.
    }

    // MARK: - ARSCNViewDelegate
    
    func setUpSceneView() {
        let configuration = ARWorldTrackingConfiguration()
        configuration.planeDetection = [.horizontal, .vertical]
        
        guard ARWorldTrackingConfiguration.supportsFrameSemantics(.personSegmentationWithDepth) else {
            fatalError("People occlusion is not supported on this device.")
        }
        configuration.frameSemantics.insert(.personSegmentationWithDepth)
        guard ARWorldTrackingConfiguration.supportsFrameSemantics(.smoothedSceneDepth) else {
            fatalError("Device doesn't support scene depth")
        }
        configuration.frameSemantics.insert(.smoothedSceneDepth)
        configuration.sceneReconstruction = .meshWithClassification

        sceneView.session.run(configuration)

        sceneView.delegate = self
        sceneView.debugOptions = [ARSCNDebugOptions.showFeaturePoints, ARSCNDebugOptions.showBoundingBoxes]
        sceneView2.scene = sceneView.scene
        
    }
    
    func addTapGestureToSceneView() {
        let tapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(addNodeToSceneView(withGestureRecognizer:)))
        sceneView.addGestureRecognizer(tapGestureRecognizer)
        }
    
    @objc func addNodeToSceneView(withGestureRecognizer recognizer: UIGestureRecognizer) {
        if counts > 0 {
            return
        }
        let tapLocation = recognizer.location(in: sceneView)
        let hitTestResults = sceneView.hitTest(tapLocation, types: .existingPlaneUsingExtent)

        // assume last hit is the floor
        guard let result = hitTestResults.last else { return }
        let resultAnchor = ARAnchor(transform: result.worldTransform)
//        resultAnchor.addChild(sphere(radius: 0.01, color: .lightGray))
        
        sceneView.session.add(anchor:resultAnchor)
        let translation = result.worldTransform.columns.3
        let x = translation.x
        let y = translation.y
        let z = translation.z
        
        nearbyFaceWithClassification(to: result.worldTransform.position) { (centerOfFace, classification) in
            // ...
            DispatchQueue.main.async {
                // 4. Compute a position for the text which is near the result location, but offset 10 cm
                // towards the camera (along the ray) to minimize unintentional occlusions of the text by the mesh.
                if classification.rawValue != 2 {
                    return
                }
//                let rayDirection = normalize(result.worldTransform.position - self.sceneView.cameraTransform.translation)
//                let textPositionInWorldCoordinates = result.worldTransform.position - (rayDirection * 0.1)

                // 5. Create a 3D text to visualize the classification result.
                    var name:String = "cropped/mesh_model.obj" //you can add node whatever
                    let tempScene = SCNScene(named: name)!
                    var geom:SCNGeometry = tempScene.rootNode.childNodes[0].geometry!
                    var boxNode:SCNNode = SCNNode(geometry: geom)
                    boxNode.position = SCNVector3(x,y,z)
                    boxNode.scale = SCNVector3Make(Float(5), Float(5), Float(5))
        //            boxNode.simdScale = 1.5
                    self.sceneView.scene.rootNode.addChildNode(boxNode)
            }
        }
    }
    
    
    func session(_ session: ARSession, didFailWithError error: Error) {
        // Present an error message to the user
        
    }
    
    func sessionWasInterrupted(_ session: ARSession) {
        // Inform the user that the session has been interrupted, for example, by presenting an overlay
        
    }
    
    func sessionInterruptionEnded(_ session: ARSession) {
        // Reset tracking and/or remove existing anchors if consistent tracking is required
        
    }
        
    func updateFrame() {
        
        // Clone pointOfView for Second View
        let pointOfView : SCNNode = (sceneView.pointOfView?.clone())!
        
        // Determine Adjusted Position for Right Eye
        let orientation : SCNQuaternion = pointOfView.orientation
        let orientationQuaternion : GLKQuaternion = GLKQuaternionMake(orientation.x, orientation.y, orientation.z, orientation.w)
        let eyePos : GLKVector3 = GLKVector3Make(1.0, 0.0, 0.0)
        let rotatedEyePos : GLKVector3 = GLKQuaternionRotateVector3(orientationQuaternion, eyePos)
        let rotatedEyePosSCNV : SCNVector3 = SCNVector3Make(rotatedEyePos.x, rotatedEyePos.y, rotatedEyePos.z)
        
        let mag : Float = 0.066 // This is the value for the distance between two pupils (in metres). The Interpupilary Distance (IPD).
        pointOfView.position.x += rotatedEyePosSCNV.x * mag
        pointOfView.position.y += rotatedEyePosSCNV.y * mag
        pointOfView.position.z += rotatedEyePosSCNV.z * mag
        
        // Set PointOfView for SecondView
        sceneView2.pointOfView = pointOfView
        
    }
    
    // UPDATE EVERY FRAME:
    func renderer(_ renderer: SCNSceneRenderer, updateAtTime time: TimeInterval) {
        DispatchQueue.main.async {
            self.updateFrame()
        }
    }
    
        
    func nearbyFaceWithClassification(to location: SIMD3<Float>, completionBlock: @escaping (SIMD3<Float>?, ARMeshClassification) -> Void) {
        guard let frame = sceneView.session.currentFrame else {
            completionBlock(nil, .none)
            return
        }
    
        var meshAnchors = frame.anchors.compactMap({ $0 as? ARMeshAnchor })
        
        // Sort the mesh anchors by distance to the given location and filter out
        // any anchors that are too far away (4 meters is a safe upper limit).
        let cutoffDistance: Float = 4.0
        meshAnchors.removeAll { distance($0.transform.position, location) > cutoffDistance }
        meshAnchors.sort { distance($0.transform.position, location) < distance($1.transform.position, location) }

        // Perform the search asynchronously in order not to stall rendering.
        DispatchQueue.global().async {
            for anchor in meshAnchors {
                for index in 0..<anchor.geometry.faces.count {
                    // Get the center of the face so that we can compare it to the given location.
                    let geometricCenterOfFace = anchor.geometry.centerOf(faceWithIndex: index)
                    
                    // Convert the face's center to world coordinates.
                    var centerLocalTransform = matrix_identity_float4x4
                    centerLocalTransform.columns.3 = SIMD4<Float>(geometricCenterOfFace.0, geometricCenterOfFace.1, geometricCenterOfFace.2, 1)
                    let centerWorldPosition = (anchor.transform * centerLocalTransform).position
                     
                    // We're interested in a classification that is sufficiently close to the given location––within 5 cm.
                    let distanceToFace = distance(centerWorldPosition, location)
                    if distanceToFace <= 0.05 {
                        // Get the semantic classification of the face and finish the search.
                        let classification: ARMeshClassification = anchor.geometry.classificationOf(faceWithIndex: index)
                        completionBlock(centerWorldPosition, classification)
                        return
                    }
                }
            }
            
            // Let the completion block know that no result was found.
            completionBlock(nil, .none)
        }
    }
    
    func sphere(radius: Float, color: UIColor) -> ModelEntity {
        let sphere = ModelEntity(mesh: .generateSphere(radius: radius), materials: [SimpleMaterial(color: color, isMetallic: false)])
        // Move sphere up by half its diameter so that it does not intersect with the mesh
        sphere.position.y = radius
        return sphere
    }
}
