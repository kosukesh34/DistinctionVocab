import Foundation

struct ExampleSentenceDTO: Decodable {
    let label: String
    let audio: String
    let text: String?
    let japaneseTranslation: String?
}
