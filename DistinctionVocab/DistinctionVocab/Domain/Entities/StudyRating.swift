import Foundation

enum StudyRating: String, CaseIterable, Sendable {
    case easy
    case good
    case hard

    var title: String {
        switch self {
        case .easy:
            return "Easy"
        case .good:
            return "Good"
        case .hard:
            return "Hard"
        }
    }
}
