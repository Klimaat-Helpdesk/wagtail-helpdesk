import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["overlay"]

  open(event) {
    event.stopPropagation();
    this.overlayTarget.classList.add('is-visible');
  }

  close(event) {
    event.stopPropagation();
    this.overlayTarget.classList.remove('is-visible');
  }
}
