/*
See LICENSE folder for this sample’s licensing information.

Abstract:
Main view controller for the AR experience.
*/

import RealityKit
import ARKit
import Foundation
import Metal
import MetalKit


@available(iOS 14.0, *)
class ViewController: UIViewController, ARSessionDelegate, MTKViewDelegate {
    
    
    @IBOutlet var arView: ARView!
    @IBOutlet weak var hideMeshButton: UIButton!
    @IBOutlet weak var resetButton: UIButton!
    @IBOutlet weak var showMenuButton: UIButton!
    
    var counts = 0
    var detected = false
    var bestPosition: SIMD3<Float> = [0, 0, 0]
    var placed = false
    
    var configuration = ARWorldTrackingConfiguration()
    var renderer: Renderer!
    var depthBuffer: CVPixelBuffer!
    var confidenceBuffer: CVPixelBuffer!
    var depth: MTLTexture?
    var frame: ARFrame?
    var addFog = false
    var tapRecognizer: UITapGestureRecognizer!
    var model: ModelEntity!
    var modelPosition: SIMD3<Float>!
    var modelName = "new_model"
    var menuItems: [UIAction] {
        return [
            UIAction(title: "Body-Complete", handler: { (_) in self.modelName = "new_model"}),
            UIAction(title: "Face-Down", handler: { (_) in self.modelName = "face-down"}),
            UIAction(title: "Face-Side", handler: { (_) in self.modelName = "mesh_model"})
            ]
    }
    var demoMenu: UIMenu {
        return UIMenu(title: "Models", image: nil, identifier: nil, options: [], children: menuItems)
    }
    
    private var computePipelineState: MTLComputePipelineState?
    private var threadsPerThreadgroup = MTLSize()
    private var threadgroupsPerGrid = MTLSize()
    
    let coachingOverlay = ARCoachingOverlayView()
    
    struct DepthFogParams {
        var orientationTransform: float2x2
        var orientationOffset: (Float, Float)
        var viewMatrix: float4x4
    }
    
    // Cache for 3D text geometries representing the classification values.
//    var modelsForClassification: [ARMeshClassification: ModelEntity] = [:]

    /// - Tag: ViewDidLoad
    override func viewDidLoad() {
        super.viewDidLoad()
        
        arView.session.delegate = self
        
        setupCoachingOverlay()

        arView.environment.sceneUnderstanding.options = []
        
        // Turn on occlusion from the scene reconstruction's mesh.
        arView.environment.sceneUnderstanding.options.insert(.occlusion)
        
        // Turn on physics for the scene reconstruction's mesh.
        arView.environment.sceneUnderstanding.options.insert(.physics)

        // Display a debug visualization of the mesh.
        arView.debugOptions.insert(.showSceneUnderstanding)
        
        // For performance, disable render options that are not required for this app.
        arView.renderOptions = [.disablePersonOcclusion, .disableDepthOfField, .disableMotionBlur]
//
        // Manually configure what kind of AR session to run since
        // ARView on its own does not turn on mesh classification.
        arView.automaticallyConfigureSession = false
        arView.isUserInteractionEnabled = true
        configuration.sceneReconstruction = .meshWithClassification
//        configuration.worldAlignment = .gravity

        configuration.environmentTexturing = .automatic
//        arView.session.run(configuration)
        navigationItem.rightBarButtonItem = UIBarButtonItem(title: "Menu", image: nil, primaryAction: nil, menu: demoMenu)
        configureButtonMenu()
        
        self.tapRecognizer = UITapGestureRecognizer(target: self, action: #selector(handleTap(_:)))
        let rotateRecognizer = UIRotationGestureRecognizer(target: self, action: #selector(rotateModel(_:)))
        let flipRecognizer = UISwipeGestureRecognizer(target: self, action: #selector(flipModel(_:)))
        arView.addGestureRecognizer(tapRecognizer)
        arView.addGestureRecognizer(rotateRecognizer)
        arView.addGestureRecognizer(flipRecognizer)
        
        
        if (addFog) {
            arView.renderCallbacks.postProcess = { [weak self] context in
                guard let self = self else { return }
                if self.computePipelineState == nil {
                    self.setupComputePipeline(targetTexture: context.targetColorTexture)
                }

                guard let computePipelineState = self.computePipelineState,
                      let encoder = context.commandBuffer.makeComputeCommandEncoder()
                else {
                    return
                }

                encoder.setComputePipelineState(computePipelineState)
                encoder.setTexture(context.sourceColorTexture, index: 0)
                encoder.setTexture(context.sourceDepthTexture, index: 1)
                encoder.setTexture(context.targetColorTexture, index: 2)
                encoder.dispatchThreadgroups(self.threadgroupsPerGrid, threadsPerThreadgroup: self.threadsPerThreadgroup)
                encoder.endEncoding()
            }
        }
        
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        // Enable the smoothed scene depth frame-semantic.
        configuration.frameSemantics = .smoothedSceneDepth

        // Run the view's session.
        arView.session.run(configuration)
        
        // The screen shouldn't dim during AR experiences.
        UIApplication.shared.isIdleTimerDisabled = true
    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        // Prevent the screen from being dimmed to avoid interrupting the AR experience.
        UIApplication.shared.isIdleTimerDisabled = true
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard self.model != nil else { return }
        if (!self.placed) {return}
        if let touch = touches.first {
            let position = touch.location(in: view)
            let query: CollisionCastQueryType = .nearest
            let mask: CollisionGroup = .default

            let translate = arView.cameraTransform.translation
            let x = translate.x
            let y = translate.y
            let z = translate.z
            let transform: SIMD3<Float> = [x, y, z]
               
            let raycasts: [CollisionCastHit] = arView.scene.raycast(
                                                               from: transform,
                                                               to: self.modelPosition,
                                                              query: query,
                                                               mask: mask,
                                                         relativeTo: nil)
            guard let raycast: CollisionCastHit = raycasts.first
            else { return }
            
            print(raycast.distance)     // Distance from the ray origin to the hit
            if (raycast.distance < 0.9){
                //create sound
//              //text pop up
                let lineHeight: CGFloat = 0.05
                let font = MeshResource.Font.systemFont(ofSize: lineHeight)
                let textMesh = MeshResource.generateText("Neck Checked!", extrusionDepth: Float(lineHeight * 0.1), font: font)
                let textMaterial = SimpleMaterial(color: UIColor.red, isMetallic: true)
                let textModel = ModelEntity(mesh: textMesh, materials: [textMaterial])
                textModel.position.z -= 1
                
                var resultWithCameraOrientation = self.arView.cameraTransform
                let messageAnchor = AnchorEntity(world: resultWithCameraOrientation.matrix)
                messageAnchor.addChild(textModel)
                self.arView.scene.addAnchor(messageAnchor, removeAfter: 3)
                
                let audioFilePath = "heartbeat.wav"
                let resource = try! AudioFileResource.load(named: audioFilePath, in: nil, inputMode: .spatial, loadingStrategy: .preload, shouldLoop: false)
                  
                let audioController = textModel.prepareAudio(resource)
                audioController.play()
            }
        }
    }
  
    func configureButtonMenu() {
        showMenuButton.menu = demoMenu
        showMenuButton.showsMenuAsPrimaryAction = true
    }
    
    private func setupComputePipeline(targetTexture: MTLTexture) {
        guard let device = MTLCreateSystemDefaultDevice(),
              let library = device.makeDefaultLibrary(),
              let postProcessingKernel = library.makeFunction(name: "inverseColorKernel"),
              let pipelineState = try? device.makeComputePipelineState(function: postProcessingKernel)
        else {
            assertionFailure()
            return
        }

        computePipelineState = pipelineState

        threadsPerThreadgroup = MTLSize(width: pipelineState.threadExecutionWidth,
                                        height: pipelineState.maxTotalThreadsPerThreadgroup / pipelineState.threadExecutionWidth,
                                        depth: 1)
        threadgroupsPerGrid = MTLSize(width: (targetTexture.width + threadsPerThreadgroup.width - 1) / threadsPerThreadgroup.width,
                                      height: (targetTexture.height + threadsPerThreadgroup.height - 1) / threadsPerThreadgroup.height,
                                      depth: 1)
        }
    
    // MARK: - MTKViewDelegate
    
    // Called whenever view changes orientation or size.
    func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {
        // Schedule the screen to be redrawn at the new size.
        renderer.drawRectResized(size: size)
    }
    
    // Implements the main rendering loop.
    func draw(in view: MTKView) {
        renderer.update()
    }
    
    
    
    @IBAction func rotateModel(_ gestureRecognizer : UIRotationGestureRecognizer) {   // Move the anchor point of the view's layer to the center of the
       // user's two fingers. This creates a more natural looking rotation.
        guard self.model != nil else { return }
            
       if gestureRecognizer.state == .began || gestureRecognizer.state == .changed {
           if self.modelName == "new_model"{
               self.model.orientation *= simd_quatf(angle: Float(gestureRecognizer.rotation), axis: SIMD3<Float>(0,0,1))
           }
           else{
               self.model.orientation *= simd_quatf(angle: Float(gestureRecognizer.rotation), axis: SIMD3<Float>(0,0,1))
           }
            
          gestureRecognizer.rotation = 0
       }
        
    }
    
    @IBAction func flipModel(_ gestureRecognizer : UISwipeGestureRecognizer) {   // Move the anchor point of the view's layer to the center of the
       // user's two fingers. This creates a more natural looking rotation.
        guard self.model != nil else { return }
            
       if gestureRecognizer.state == .ended {
           gestureRecognizer.numberOfTouchesRequired = 1
           if (gestureRecognizer.direction == .left) {
               self.model.orientation *= simd_quatf(angle: Float(Double.pi/2), axis: SIMD3<Float>(0,0,1))
               self.model.orientation *= simd_quatf(angle: Float(Double.pi/2), axis: SIMD3<Float>(0,0,1))
           }
           if (gestureRecognizer.direction == .right) {
               self.model.orientation *= simd_quatf(angle: Float(-Double.pi/2), axis: SIMD3<Float>(0,0,1))
               self.model.orientation *= simd_quatf(angle: Float(-Double.pi/2), axis: SIMD3<Float>(0,0,1))
           }
       }
        
    }
    
    /// Places virtual-text of the classification at the touch-location's real-world intersection with a mesh.
    /// Note - because classification of the tapped-mesh is retrieved asynchronously, we visualize the intersection
    /// point immediately to give instant visual feedback of the tap.
    @objc
    func handleTap(_ sender: UITapGestureRecognizer) {
        // 1. Perform a ray cast against the mesh.
        // Note: Ray-cast option ".estimatedPlane" with alignment ".any" also takes the mesh into account.
        if self.placed {
            return
        }
        let tapLocation = sender.location(in: arView)
        if let result = arView.raycast(from: tapLocation, allowing: .estimatedPlane, alignment: .horizontal).first {
            // ...
            // 2. Visualize the intersection point of the ray with the real-world surface.
            let resultAnchor = AnchorEntity(world: result.worldTransform)
            resultAnchor.addChild(sphere(radius: 0.01, color: .blue))
            
            arView.scene.addAnchor(resultAnchor)

            // 3. Try to get a classification near the tap location.
            //    Classifications are available per face (in the geometric sense, not human faces).
            nearbyFaceWithClassification(to: result.worldTransform.position) { (centerOfFace, classification) in
                // ...
                DispatchQueue.main.async {
                    // 4. Compute a position for the text which is near the result location, but offset 10 cm
                    // towards the camera (along the ray) to minimize unintentional occlusions of the text by the mesh.
                    if classification.rawValue != 2 {
                        return
                    }
                    let rayDirection = normalize(result.worldTransform.position - self.arView.cameraTransform.translation)
                    let textPositionInWorldCoordinates = result.worldTransform.position - (rayDirection * 0.1)
                    self.modelPosition = textPositionInWorldCoordinates

                    // 5. Create a 3D text to visualize the classification result.
                    let textEntity = self.model(for: classification, to: resultAnchor.position.z)

                    // 7. Place the text, facing the camera.
//                    var resultWithCameraOrientation = self.arView.cameraTransform
//                    resultWithCameraOrientation.translation = textPositionInWorldCoordinates
//                    let textAnchor = AnchorEntity(world: resultWithCameraOrientation.matrix)
                    let textAnchor = AnchorEntity(world: textPositionInWorldCoordinates)
                    textAnchor.addChild(textEntity!)
                    self.arView.scene.addAnchor(textAnchor)
                    self.placed = true
                    self.tapRecognizer.isEnabled = false

                    // 8. Visualize the center of the face (if any was found) for three seconds.
                    //    It is possible that this is nil, e.g. if there was no face close enough to the tap location.
                    if let centerOfFace = centerOfFace {
                        let faceAnchor = AnchorEntity(world: centerOfFace)
                        faceAnchor.addChild(self.sphere(radius: 0.01, color: classification.color))
                        self.arView.scene.addAnchor(faceAnchor)
                    }
                }
            }
        }
    }
    
    @IBAction func resetButtonPressed(_ sender: Any) {
        let anchors = self.arView.scene.anchors
        for anchor in anchors{
            self.arView.scene.removeAnchor(anchor)
        }
        self.placed = false
        self.tapRecognizer.isEnabled = true
    }
    
    
    @IBAction func toggleMeshButtonPressed(_ button: UIButton) {
        addFog = !addFog
    }
    
    
    func nearbyFaceWithClassification(to location: SIMD3<Float>, completionBlock: @escaping (SIMD3<Float>?, ARMeshClassification) -> Void) {
        guard let frame = arView.session.currentFrame else {
            completionBlock(nil, .none)
            return
        }
    
        var meshAnchors = frame.anchors.compactMap({ $0 as? ARMeshAnchor })
        
        // Sort the mesh anchors by distance to the given location and filter out
        // any anchors that are too far away (4 meters is a safe upper limit).
//        let cutoffDistance: Float = 4.0
//        meshAnchors.removeAll { distance($0.transform.position, location) > cutoffDistance }
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
    
    func session(_ session: ARSession, didFailWithError error: Error) {
        guard error is ARError else { return }
        let errorWithInfo = error as NSError
        let messages = [
            errorWithInfo.localizedDescription,
            errorWithInfo.localizedFailureReason,
            errorWithInfo.localizedRecoverySuggestion
        ]
        let errorMessage = messages.compactMap({ $0 }).joined(separator: "\n")
        DispatchQueue.main.async {
            // Present an alert informing about the error that has occurred.
            let alertController = UIAlertController(title: "The AR session failed.", message: errorMessage, preferredStyle: .alert)
            let restartAction = UIAlertAction(title: "Restart Session", style: .default) { _ in
                alertController.dismiss(animated: true, completion: nil)
                self.resetButtonPressed(self)
            }
            alertController.addAction(restartAction)
            self.present(alertController, animated: true, completion: nil)
        }
    }
    
    // eliminate mesh once a model is placed
    func session(_ session: ARSession, didUpdate anchors: [ARAnchor]) {
        let isShowingMesh = arView.debugOptions.contains(.showSceneUnderstanding)
        if isShowingMesh && placed {
            arView.debugOptions.remove(.showSceneUnderstanding)
        }
        if (addFog) {
            arView.renderCallbacks.postProcess = { [weak self] context in
                guard let self = self else { return }
                if self.computePipelineState == nil {
                    self.setupComputePipeline(targetTexture: context.targetColorTexture)
                }

                guard let computePipelineState = self.computePipelineState,
                      let encoder = context.commandBuffer.makeComputeCommandEncoder()
                else {
                    return
                }

                encoder.setComputePipelineState(computePipelineState)
                encoder.setTexture(context.sourceColorTexture, index: 0)
                encoder.setTexture(context.sourceDepthTexture, index: 1)
                encoder.setTexture(context.targetColorTexture, index: 2)
                encoder.dispatchThreadgroups(self.threadgroupsPerGrid, threadsPerThreadgroup: self.threadsPerThreadgroup)
                encoder.endEncoding()
            }
        }
    }
        
    func model(for classification: ARMeshClassification, to location: Float) -> ModelEntity? {
        if classification.rawValue == 2 {
            let model = try! ModelEntity.loadModel(named: self.modelName)
            model.generateCollisionShapes(recursive: true)
            self.arView.installGestures(.rotation, for: model as Entity & HasCollision)
            model.scale = SIMD3(Float(1), Float(1), Float(1))
//            model.transform.rotation = simd_quatf(angle: -.pi/6,    /* -45 Degrees */
//                                                  axis: [0,1,0])
//            model.transform.rotation += simd_quatf(angle: -.pi/2,    /* -45 Degrees */
//                                                  axis: [0,0,1])
//            model.position.z -= 2
            self.model = model
//            model.position.y -= 2
//            model.setOrientation(self.frame?.camera, relativeTo: nil)
            return model
        }
      
        return nil
    }
    
    func sphere(radius: Float, color: UIColor) -> ModelEntity {
        let sphere = ModelEntity(mesh: .generateSphere(radius: radius), materials: [SimpleMaterial(color: color, isMetallic: false)])
        // Move sphere up by half its diameter so that it does not intersect with the mesh
        sphere.position.y = radius
        return sphere
    }
}
