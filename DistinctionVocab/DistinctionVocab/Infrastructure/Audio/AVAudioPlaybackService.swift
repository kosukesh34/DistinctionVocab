import AVFoundation
import Observation

@MainActor
@Observable
final class AVAudioPlaybackService: NSObject, AudioPlaybackManaging {
    private(set) var isPlaying = false
    private(set) var currentlyPlayingResourcePath: String?

    private let audioResourceRepository: AudioResourceRepositoryProtocol
    private var audioPlayer: AVAudioPlayer?

    init(audioResourceRepository: AudioResourceRepositoryProtocol) {
        self.audioResourceRepository = audioResourceRepository
        super.init()
        configureAudioSession()
    }

    func play(resource: AudioResourceReference) {
        guard let audioURL = audioResourceRepository.resolveURL(for: resource) else {
            print("Audio not found: \(resource.relativePath)")
            return
        }

        stopPlayback()

        do {
            audioPlayer = try AVAudioPlayer(contentsOf: audioURL)
            audioPlayer?.delegate = self
            currentlyPlayingResourcePath = resource.relativePath
            isPlaying = true
            audioPlayer?.play()
        } catch {
            print("Playback error: \(error)")
            resetPlaybackState()
        }
    }

    func stop() {
        stopPlayback()
    }

    func toggle(resource: AudioResourceReference) {
        let isSameResourcePlaying =
            isPlaying && currentlyPlayingResourcePath == resource.relativePath

        if isSameResourcePlaying {
            stop()
        } else {
            play(resource: resource)
        }
    }

    private func configureAudioSession() {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("Audio session error: \(error)")
        }
    }

    private func stopPlayback() {
        audioPlayer?.stop()
        audioPlayer = nil
        resetPlaybackState()
    }

    private func resetPlaybackState() {
        isPlaying = false
        currentlyPlayingResourcePath = nil
    }
}

extension AVAudioPlaybackService: AVAudioPlayerDelegate {
    nonisolated func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        Task { @MainActor in
            resetPlaybackState()
        }
    }
}
