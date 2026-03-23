
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["videoPanel", "textPanel", "videoBtn", "textBtn", "iframe"]

  connect() {
    if (this.hasIframeTarget && this.iframeTarget?.dataset?.src) {
      this.showVideo()
    } else {
      this.showText()
    }
  }

  showVideo() {
    this._setSelected(true)
    this._show(this.videoPanelTarget)
    this._hide(this.textPanelTarget)

    if (this.hasIframeTarget) {
      const src = this.iframeTarget.getAttribute("src")
      if (!src) this.iframeTarget.setAttribute("src", this.iframeTarget.dataset.src)
    }
  }

  showText() {
    this._setSelected(false)
    this._hide(this.videoPanelTarget)
    this._show(this.textPanelTarget)

    if (this.hasIframeTarget && this.iframeTarget.getAttribute("src")) {
      this.iframeTarget.setAttribute("src", "")
    }
  }

  _show(el)   { el.hidden = false }
  _hide(el)   { el.hidden = true }
  _setSelected(videoSelected) {
    if (this.hasVideoBtnTarget) this.videoBtnTarget.setAttribute("aria-selected", String(videoSelected))
    if (this.hasTextBtnTarget)  this.textBtnTarget.setAttribute("aria-selected", String(!videoSelected))
  }
}
