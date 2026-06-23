import Foundation

@MainActor
protocol AudioPlaybackManaging: AnyObject {
    var isPlaying: Bool { get }
    var currentlyPlayingResourcePath: String? { get }

    func play(resource: AudioResourceReference)
    func stop()
    func toggle(resource: AudioResourceReference)
}
