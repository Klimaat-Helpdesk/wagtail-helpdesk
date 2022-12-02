import Controller from '../modules/controller';

export default class SocialShareButtonsController extends Controller {

  init() {
    this.urlInputElement = this.element.getElementsByClassName("js-url-input")[0];
    this.titleInputElement = this.element.getElementsByClassName("js-title-input")[0];
    this.codeTextareaElement = this.element.getElementsByClassName("js-code-textarea")[0];

    this.updateCode();
    this.initEventHandlers();
  }

  initEventHandlers() {
    let self = this;
    this.titleInputElement.addEventListener("keyup", event => {
      self.updateCode();
    });
  }

  updateCode() {
    this.codeTextareaElement.value = `<iframe src="${this.urlInputElement.value}?title=${this.titleInputElement.value}" style="width: 100%; height: 100px;"></iframe>`
  }
}
