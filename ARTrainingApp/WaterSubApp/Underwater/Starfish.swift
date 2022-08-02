/*
See LICENSE folder for this sample’s licensing information.

Abstract:
Spawns and manages starfish.
*/
import RealityKit

struct StarfishComponent: RealityKit.Component {}

extension UnderwaterView {

    func setupStarfish() {
        Entity.loadModelAsync(named: "face-down")
            .sink(receiveValue: { [weak self] face in
                guard let self = self else { return }
                guard let faceModel = face.model else {
                    assertionFailure("No mesh on the human model")
                    return
                }
                let entity = face
                if self.features.contains(.highLevelsOfDetail) {
                    entity.components.set(LevelOfDetailComponent([
                        .init(maxDistance: 1E2, model: faceModel)
                    ]))
                }
                
                self.setupStarfishScattering(entity)
            }).store(in: &cancellables)
    }

    fileprivate func setupStarfishScattering(_ starfish: Entity) {
        starfish.components[StarfishComponent.self] = StarfishComponent()

        scattering.add(Scattering.ScatteringSet(spawner: StarfishSpawner(
            entity: starfish,
            view: self
        )))
    }

    fileprivate struct StarfishSpawner: ScatteringSpawner {

        private static let query = EntityQuery(where: .has(StarfishComponent.self))

        let entity: Entity
        weak var view: UnderwaterView?

        var scale: Float = 1.0

        mutating func randomize() {
            scale = .random(in: 0.3..<1.0)
        }

        func attempt(_ location: Scattering.CandidateLocation) -> Entity? {
            guard let view = self.view else { return nil }

            // Can't spawn too close to the other ones.
            guard view.scene.performQuery(Self.query).filter({
                $0.isDistanceWithinThreshold(from: location.position, max: 0.3)
            }).isEmpty else { return nil }

            // Can't stick to the ceiling.
            if dot(location.normal, .init(0, 1, 0)) < -0.1 { return nil }
            
            // Only spawn on horizontal surfaces.
            guard location.normal.y > 0.7 else { return nil }

            let clone = entity.clone(recursive: true)
            clone.scale *= .init(repeating: scale)
            clone.position = location.position
//            clone.orientation = .init(from: .init(0, 1, 0), to: location.normal)
            return clone
        }
    }
}
