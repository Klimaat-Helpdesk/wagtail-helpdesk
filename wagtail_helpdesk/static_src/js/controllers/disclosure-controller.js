import {Controller} from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["region"]

  toggleRegion(event) {
    if (event.target.getAttribute('aria-expanded') === 'true') {
      this.regionTarget.setAttribute('aria-hidden', true)
      event.target.setAttribute('aria-expanded', false)
    } else {
      this.regionTarget.setAttribute('aria-hidden', false)
      event.target.setAttribute('aria-expanded', true)
    }
    const rect = this.regionTarget.getBoundingClientRect()
    window.scroll({ top: (window.pageYOffset + rect.top) - (window.innerHeight / 3), left: 0, behavior: 'smooth' })
  }
}
