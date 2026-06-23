import Foundation

struct BundleAudioResourceRepository: AudioResourceRepositoryProtocol {
    private let bundle: Bundle

    init(bundle: Bundle = .main) {
        self.bundle = bundle
    }

    func resolveURL(for resource: AudioResourceReference) -> URL? {
        let pathComponents = resource.relativePath.split(separator: "/").map(String.init)
        guard let fileName = pathComponents.last else { return nil }

        let bookIdentifier = pathComponents.dropLast().joined(separator: "/")
        let pathExtension = (fileName as NSString).pathExtension
        let resourceName = (fileName as NSString).deletingPathExtension

        let candidateSubdirectories = [
            "Audio/\(bookIdentifier)",
            bookIdentifier,
            "Resources/Audio/\(bookIdentifier)"
        ]

        for subdirectory in candidateSubdirectories {
            if let resolvedURL = bundle.url(
                forResource: resourceName,
                withExtension: pathExtension,
                subdirectory: subdirectory
            ) {
                return resolvedURL
            }
        }

        return nil
    }
}
