import Foundation

protocol AudioResourceRepositoryProtocol: Sendable {
    func resolveURL(for resource: AudioResourceReference) -> URL?
}
