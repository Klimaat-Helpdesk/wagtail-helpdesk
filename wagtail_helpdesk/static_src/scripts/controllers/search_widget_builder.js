import Controller from '../modules/controller';
import copy from 'copy-to-clipboard';

export default class SearchWidgetBuilderController extends Controller {

  init() {
    this.urlInputElement = this.element.querySelector(".js-url-input");
    this.titleInputElement = this.element.querySelector(".js-title-input");
    this.codeTextareaElement = this.element.querySelector(".js-code-textarea");
    this.copyCodeButton = this.element.querySelector(".js-copy-code-button");
    this.message = this.element.querySelector(".js-message");

    this.updateCode();
    this.initEventHandlers();
  }

  succesMessage(element) {
    element.style.display = "inline";
    setTimeout(function () {
      element.style.display = "none";
    }, 1200);
  }

  initEventHandlers() {
    let self = this;
    this.titleInputElement.addEventListener("keyup", event => {
      self.updateCode();
    });

    this.copyCodeButton.addEventListener("click", event => {
      copy(this.codeTextareaElement.value);
      this.succesMessage(this.message);
    });
  }

  updateCode() {
    this.codeTextareaElement.value = `<iframe src="${this.urlInputElement.value}?title=${this.titleInputElement.value}" style="width: 100%; height: 100px;"></iframe>`
  }
}

