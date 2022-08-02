/*
See LICENSE folder for this sample’s licensing information.

Abstract:
ARView subclass for the underwater scene.
*/

import ARKit
import Combine
import SwiftUI
import RealityKit

enum Feature: String, CaseIterable {
    case diverCharacter
    case postProcessing
    case octopus
    case seaweed
    case meshAnchorTacker
    case starfish
    case clownFish
    case yellowTangFish
    case krill
    case highLevelsOfDetail
    case flockLeader
    case rkSceneUnderstanding

    var key: String { "feature_\(rawValue)" }

    var enabled: Bool? {
        guard UserDefaults.standard.object(forKey: key) != nil else { return nil }
        return UserDefaults.standard.bool(forKey: key)
    }

    var hasMovement: Bool {
        switch self {
        case .clownFish, .yellowTangFish, .flockLeader: return true
        default: return false
        }
    }

    var hasScattering: Bool {
        switch self {
        case .octopus, .seaweed, .starfish: return true
        default: return false
        }
    }

    static let features: Set<Feature> = { .init(Feature.allCases.filter { $0.enabled ?? true }) }()
}

class UnderwaterView: ARView, ARSessionDelegate {

    init(frame: CGRect, settings: Settings) {
        self.settings = settings
        super.init(frame: frame)
    }

    required init?(coder decoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    required init(frame frameRect: CGRect) {
        fatalError("init(frame:) has not been implemented")
    }

    var features: Set<Feature> { Feature.features }

    struct DebugOptions {
        var showSceneUnderstanding = false
        var showPhysics = false
        var showStatistics = false
        var throttle = false

    }

    struct DebugOptionsView: SwiftUI.View {
        var options: Binding<DebugOptions>

        var body: some SwiftUI.View {
            VStack {
                Toggle("show scene understanding", isOn: options.showSceneUnderstanding)
                Toggle("show physics", isOn: options.showPhysics)
                Toggle("show stats", isOn: options.showStatistics)
                Toggle("throttle", isOn: options.throttle)
            }
        }
    }

    var arView: ARView { return self }

    let settings: Settings

    private var debugThrottle: Cancellable?

    func set(debugThrottle: Bool) {
        let minFPS = 10.0
        let maxFPS = 120.0
        guard debugThrottle else { self.debugThrottle = nil; return }
        var debugThrottleTime = 0.0
        self.debugThrottle = scene.subscribe(to: SceneEvents.Update.self) { event in
            Thread.sleep(forTimeInterval: 1.0 / (minFPS + 0.5 * (1.0 + sin(debugThrottleTime)) * (maxFPS - minFPS)))
            debugThrottleTime += event.deltaTime
        }
    }

    var cancellables = [AnyCancellable]()
    var gameState = GameState()

    var character: Character?

    var foodPool: FoodPool!

    lazy var fishAnchor: AnchorEntity = {
        let fishAnchor = AnchorEntity(world: .zero)
        scene.addAnchor(fishAnchor)
        return fishAnchor
    }()

    var meshAnchorTracker: MeshAnchorTracker?
    var postProcessing: PostProcessing?
    var scattering = Scattering()
    var camera: AnchorEntity?

    func session(_ session: ARSession, didAdd anchors: [ARAnchor]) {
        updateAnchors(anchors: anchors)
    }

    func session(_ session: ARSession, didUpdate anchors: [ARAnchor]) {
        updateAnchors(anchors: anchors)
    }

    func session(_ session: ARSession, didRemove anchors: [ARAnchor]) {
        for anchor in anchors.compactMap({ $0 as? ARMeshAnchor }) {
            meshAnchorTracker?.remove(anchor)
        }
    }

    func updateAnchors(anchors: [ARAnchor]) {

        for anchor in anchors.compactMap({ $0 as? ARMeshAnchor }) {
            meshAnchorTracker?.update(anchor)
        }
        if settings.scattering {
            scattering.update(from: anchors, view: self)
        }
    }

    func session(_ session: ARSession, didUpdate frame: ARFrame) {
        postProcessing?.update(frame)
        camera?.transform = .init(matrix: frame.camera.transform)
    }

    var debugOptionsSub: Cancellable?

    func setup() {
        MetalLibLoader.initializeMetal()
        setupDebugOptionsSubscription()
        configureWorldTracking()
        loadModels()
        setupPhysicsOrigin()
        setupCameraTracker()
    }

    private func setupDebugOptionsSubscription() {
        debugOptionsSub = settings.$view.sink { [weak self] in
            let setDebugOption = { (option: ARView.DebugOptions, value: Bool) -> Void in
                if value {
                    self?.debugOptions.insert(option)
                } else {
                    self?.debugOptions.remove(option)
                }
            }
            setDebugOption(.showSceneUnderstanding, $0.showSceneUnderstanding)
            setDebugOption(.showPhysics, $0.showPhysics)
            setDebugOption(.showStatistics, $0.showStatistics)
            self?.set(debugThrottle: $0.throttle)
        }
    }

    private func setupPhysicsOrigin() {

        // Set up a good scale for physics. For more information see: https://developer.apple.com/documentation/realitykit/handling_different-sized_objects_in_physics_simulations#3694567

        let physicsOrigin = Entity()
        physicsOrigin.scale = .init(repeating: 0.1)
        let anchor = AnchorEntity(world: SIMD3<Float>())
        anchor.addChild(physicsOrigin)
        scene.addAnchor(anchor)
        self.physicsOrigin = physicsOrigin
    }

    private func setupCameraTracker() {
        let camera = AnchorEntity(world: SIMD3<Float>())
        self.camera = camera
        camera.components.set(CameraComponent())
        scene.addAnchor(camera)
    }

    private func configureWorldTracking() {
        let configuration = ARWorldTrackingConfiguration()

        let sceneReconstruction: ARWorldTrackingConfiguration.SceneReconstruction = .mesh
        if ARWorldTrackingConfiguration.supportsSceneReconstruction(sceneReconstruction) {
            configuration.sceneReconstruction = sceneReconstruction
            meshAnchorTracker = .init(arView: self)
        }

        let frameSemantics: ARConfiguration.FrameSemantics = [.smoothedSceneDepth, .sceneDepth]
        if ARWorldTrackingConfiguration.supportsFrameSemantics(frameSemantics) {
            configuration.frameSemantics.insert(frameSemantics)
            postProcessing = .init(arView: self)
        }

        configuration.planeDetection.insert(.horizontal)
        session.run(configuration)
        defer { session.delegate = self }

        arView.renderOptions.insert(.disableMotionBlur)
        if features.contains(.rkSceneUnderstanding) {
            arView.environment.sceneUnderstanding.options.insert([.collision, .physics, .receivesLighting, .occlusion])
        }
    }

    private func loadModels() {

//        setupStarfish()

        let singleTap = UITapGestureRecognizer(target: self, action: #selector(handleTap))
        addGestureRecognizer(singleTap)
    }

    private func anchor(for entity: Entity) -> AnchorEntity {
        let bounds = entity.visualBounds(relativeTo: nil)
        let anchor = AnchorEntity(.plane(.horizontal, classification: .any, minimumBounds: .init(bounds.extents.x, bounds.extents.y)))
        return anchor
    }

//    @objc
//    func handleTap(_ gestureRecognizer: UIGestureRecognizer) {
//        let location = gestureRecognizer.location(in: gestureRecognizer.view)
////        if location.x <= 0.1 * bounds.height {
////            character?.controllerJump = true
////        } else {
//        foodPool?.handleTap(gestureRecognizer)
////        }
//    }
    
    @objc
    func handleTap(_ gestureRecognizer: UIGestureRecognizer) {

        let tapLocation = gestureRecognizer.location(in: gestureRecognizer.view)
        
        if let result = arView.raycast(from: tapLocation, allowing: .estimatedPlane, alignment: .horizontal).first {
            // ...
            // 2. Visualize the intersection point of the ray with the real-world surface.
            let resultAnchor = AnchorEntity(world: result.worldTransform)
            resultAnchor.addChild(sphere(radius: 0.01, color: .blue))
            
            arView.scene.addAnchor(resultAnchor)
            print("tap location:", result.worldTransform.position.z)

            let rayDirection = normalize(result.worldTransform.position - self.arView.cameraTransform.translation)
            let textPositionInWorldCoordinates = result.worldTransform.position - (rayDirection * 0.1)

            // 5. Create a 3D text to visualize the classification result.
            let textEntity = self.model()

            // 7. Place the text, facing the camera.
//            var resultWithCameraOrientation = self.arView.cameraTransform
//            resultWithCameraOrientation.translation = textPositionInWorldCoordinates
//            let textAnchor = AnchorEntity(world: resultWithCameraOrientation.matrix)
            let textAnchor = AnchorEntity(world: textPositionInWorldCoordinates)
            textAnchor.addChild(textEntity!)
            self.arView.scene.addAnchor(textAnchor)
        }
    }
    
    
    func sphere(radius: Float, color: UIColor) -> ModelEntity {
        let sphere = ModelEntity(mesh: .generateSphere(radius: radius), materials: [SimpleMaterial(color: color, isMetallic: false)])
        // Move sphere up by half its diameter so that it does not intersect with the mesh
        sphere.position.y = radius
        return sphere
    }
    
    func model() -> ModelEntity? {
        let model = try! ModelEntity.loadModel(named: "face-down")
        model.scale = SIMD3(Float(1), Float(1), Float(1))
//            model.orientation = simd_quatf(angle: -.pi/4,    /* -45 Degrees */
//                                           axis: [1,1,1])
//        model.transform.rotation = simd_quatf(angle: -.pi/6.2,    /* -45 Degrees */
//                                              axis: [0,1,0])
//        model.transform.rotation += simd_quatf(angle: -.pi/2,    /* -45 Degrees */
//                                              axis: [0,0,1])
        model.position.z -= 1
//        let delta_z = model.visualBounds(relativeTo: nil).extents.z * 1.36 * 2
//        model.position.z = location + delta_z

        return model
    }
}

extension CollisionGroup {
    static var fishGroup = CollisionGroup(rawValue: 15)
    static var foodGroup = CollisionGroup(rawValue: 16)
}

extension ARMeshAnchor {
    var boundingBox: BoundingBox {
        self.geometry.vertices.asSIMD3(ofType: Float.self).reduce(BoundingBox(), { return $0.union($1) })
    }
}

extension Publisher {

    func sink(_ receiveValue: @escaping ((Self.Output) -> Void)) -> AnyCancellable {
        sink(
            receiveCompletion: { result in
                switch result {
                case .failure(let error): assertionFailure("\(error)")
                default: return
                }
            },
            receiveValue: receiveValue
        )
    }
}

extension Publisher {
    func sink(receiveValue: @escaping ((Self.Output) -> Void)) -> AnyCancellable {
        sink(
            receiveCompletion: { result in
                switch result {
                case .failure(let error): assertionFailure("\(error)")
                default: return
                }
            },
            receiveValue: receiveValue
        )
    }
}

struct CameraComponent: Component {

    static let query = EntityQuery(where: .has(Self.self))
}
