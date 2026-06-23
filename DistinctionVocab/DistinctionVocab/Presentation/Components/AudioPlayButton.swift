import SwiftUI

struct AudioPlayButton: View {
    let audioResource: AudioResourceReference
    var iconSize: CGFloat = 44
    var tintColor: Color = .accentColor

    @Environment(AVAudioPlaybackService.self) private var audioPlaybackService

    private var isCurrentlyPlaying: Bool {
        audioPlaybackService.isPlaying
            && audioPlaybackService.currentlyPlayingResourcePath == audioResource.relativePath
    }

    var body: some View {
        Button {
            audioPlaybackService.toggle(resource: audioResource)
        } label: {
            Image(systemName: isCurrentlyPlaying ? "pause.circle.fill" : "play.circle.fill")
                .font(.system(size: iconSize))
                .foregroundStyle(tintColor)
                .symbolEffect(.pulse, isActive: isCurrentlyPlaying)
        }
        .buttonStyle(.plain)
        .accessibilityLabel(isCurrentlyPlaying ? "一時停止" : "再生")
    }
}
