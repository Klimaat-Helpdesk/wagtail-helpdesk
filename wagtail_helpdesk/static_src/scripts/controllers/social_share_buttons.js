import Controller from '../modules/controller';

export default class SocialShareButtonsController extends Controller {

  init() {
      this.initializeButtons();
  }

  initializeButtons() {
    const url = window.location.href;
    const title = document.title;
    const shareButtons = document.querySelectorAll(".js-social-share-button");
    if (!shareButtons) { return };
    shareButtons.forEach(button => {
      const socialMediaPlatform = button.dataset.socialPlatform
      let link = ""
      if(socialMediaPlatform === "facebook") {
        link = `https://www.facebook.com/sharer/sharer.php?u=${url}`
      } else if (socialMediaPlatform === "twitter") {
        link = `http://twitter.com/share?&url=${url}`
      } else if (socialMediaPlatform === "linkedin") {
        link = `https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${title}`
      } else if (socialMediaPlatform === "whatsapp") {
        link = `https://wa.me/?text=${url}`;
      }
      button.setAttribute("href", link);
    })
  }

}
