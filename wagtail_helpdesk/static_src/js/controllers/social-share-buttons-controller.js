import {Controller} from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["link"]

  connect() {
    const url = window.location.href;
    const title = document.title;
    this.linkTargets.forEach(element => {
      const socialMediaPlatform = element.dataset.socialPlatform;
      let link = ""
      if (socialMediaPlatform === "facebook") {
        link = `https://www.facebook.com/sharer/sharer.php?u=${url}`
      } else if (socialMediaPlatform === "twitter") {
        link = `http://twitter.com/share?&url=${url}`
      } else if (socialMediaPlatform === "linkedin") {
        link = `https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${title}`
      } else if (socialMediaPlatform === "whatsapp") {
        link = `https://wa.me/?text=${url}`;
      }
      element.setAttribute("href", link);
    })
  }
}