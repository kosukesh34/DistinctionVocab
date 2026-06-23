import Foundation

/// アプリバンドル内の音声ファイルへの参照。
struct AudioResourceReference: Hashable, Sendable {
    let relativePath: String
}
