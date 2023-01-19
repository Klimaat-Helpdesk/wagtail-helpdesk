import {Controller} from "@hotwired/stimulus"
import copy from 'copy-to-clipboard'


export default class extends Controller {
  static targets = ["url", "title", "code", "example", "message"]

  connect() {
    this.updateCode();
  }

  keyup(event) {
    this.updateCode();
  }

  copy(event) {
    var self = this;
    copy(this.codeTarget.value);

    // Show copy message
    this.messageTarget.style.display = "inline";
    setTimeout(function () {
      self.messageTarget.style.display = "none";
    }, 1200);
  }

  clear() {
    this.titleTarget.value = "";
    this.titleTarget.focus();

    this.updateCode();
  }

  updateCode() {
    this.codeTarget.value = `<iframe src="${this.urlTarget.value}?title=${this.titleTarget.value}" style="width: 100%; height: 120px;"></iframe>`
    this.exampleTarget.innerHTML = this.codeTarget.value;
  }
}