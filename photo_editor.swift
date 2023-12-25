import SwiftUI

struct ContentView: View {
    @State private var image: Image?
    @State private var filter = "none"

    var body: some View {
        VStack {
            if image != nil {
                Image(uiImage: image!)
                    .resizable()
                    .frame(width: 300, height: 300)
            }
            Button ("Edit") {
                self.image = UIImage(named: "photo.jpg")

            }
            .sheet(item: $image) {
                image in EditImage(image: image)

            }
        }
    }
}

struct EditImage: UIViewControllerRepresentable {
    let image: UIImage

    func makeUIViewController(context: Context) -> EditImageViewController {
        return EditImageViewController()
    }

    func updateUIViewController(_uiViewController: EditImageViewController, context: Context) {
        uiViewController.image = image
    }
}

class EditImageViewController: UIViewController{
    @IBOutlet weak var imageView: UIImageView!

    override func viewDidLoad() {
        super.viewDidLoad()

        imageView.image = image

        let filterMenu = UIMenu(title: "Filter", children: [
            UIImage.filterMenuFilter(name: "none"),
            UIImage.filterMenuFilter(name: "Sepia"),
            UIImage.filterMenuFilter(name: "Grayscale"),
        ])

        let editMenu = UIMenu(title: "Edit", children: [
            UIImage.editMenuCrop(),
            UIImage.editMenuResize(width:(max: 1024, min: 200)),
            UIImage.editMenuRotate(by: 90),
            UIImage.editMenuFlip(horizontal: true, vertical: true)
        ])

            image.menu = UIMenu(titles: ["Filter", "Edit"], children: [filterMenu, editMenu])
    }
}
