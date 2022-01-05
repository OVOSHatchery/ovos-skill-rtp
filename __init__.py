from ovos_plugin_common_play.ocp import MediaType, PlaybackType
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    ocp_search, ocp_featured_media


class RTPSkill(OVOSCommonPlaybackSkill):
    def __init__(self):
        super().__init__("RTP")
        self.supported_media = [MediaType.TV, MediaType.GENERIC]
        self.skill_icon = self.default_bg = "https://cdn-images.rtp.pt/common/img/channels/logos/gray-negative/horizontal/rtp.png"

    # matching
    def match_skill(self, phrase, media_type):
        score = 0
        if self.lang.startswith("pt"):
            score += 20
        if self.voc_match(phrase, "rtp") or media_type == MediaType.TV:
            score += 50
        if self.voc_match(phrase, "tv") or media_type == MediaType.TV:
            score += 30
            if self.lang.startswith("pt"):
                score += 30
        return score

    @property
    def javascript(self):
        return """
        document.getElementsByClassName("bg-gray-list padding-bottom-65")[0].remove();
        document.getElementById("acess-buttons-container").remove();
        document.getElementsByClassName("container-menu-rtp")[0].remove();
        document.getElementsByClassName("col-xs-12 text-center promo-btns")[0].remove();
        document.getElementsByClassName("col-xs-12 text-center text-white")[0].remove();
        document.getElementsByClassName("col-xs-12 text-center promo-copy")[0].remove();
        document.getElementsByClassName("bg-footer")[0].remove();
        document.getElementById("LiveContentData").remove();
        """

    @ocp_search()
    def search_db(self, phrase, media_type):
        score = self.match_skill(phrase, media_type)
        if self.voc_match(phrase, "rtp"):
            yield {
                "match_confidence": score,
                "media_type": MediaType.TV,
                "playlist": self.featured_media(),
                "playback": PlaybackType.WEBVIEW,
                "skill_icon": self.skill_icon,
                "image": self.skill_icon,
                "bg_image": self.default_bg,
                "title": "RTP (TV Channel Playlist)",
                "author": "RTP"
            }

    @ocp_featured_media()
    def featured_media(self):
        channels = {
            "rtp1": {
                "name": "RTP1",
                "img":  "https://cdn-images.rtp.pt/common/img/channels/logos/color/horizontal/5-563718101410.png"
            },
            "rtp2": {
                "name": "RTP2",
                "img": "https://cdn-images.rtp.pt/common/img/channels/logos/color/horizontal/3-363718101410.png"
            },
            "rtp3": {
                "name": "RTP3",
                "img": "https://cdn-images.rtp.pt/common/img/channels/logos/color/horizontal/64-393818101410.png"
            },
            "rtpinternacional": {
                "name": "RTP Internacional",
                "img": "https://cdn-images.rtp.pt/common/img/channels/logos/color/horizontal/120-344318101410.png"
            },
            "rtpmemoria": {
                "name": "RTP Memoria",
                "img": "https://cdn-images.rtp.pt/common/img/channels/logos/color/horizontal/80-584819141705.png"
            },
            "rtpmadeira": {
                "name": "RTP Madeira",
                "img": "https://cdn-images.rtp.pt/common/img/channels/logos/color/horizontal/107-443519141305.png"
            },
            "rtpacores": {
                "name": "RTP Açores",
                "img": "https://cdn-images.rtp.pt/common/img/channels/logos/color/horizontal/106-563419141305.png"
            },
            "rtpafrica": {
                "name": "RTP Africa",
                "img": "https://cdn-images.rtp.pt/common/img/channels/logos/color/horizontal/27-363219141305.png"
            }
        }
        return [{
            "title": ch["name"],
            "image": ch["img"],
            "match_confidence": 80,
            "media_type": MediaType.TV,
            "uri": f"https://www.rtp.pt/play/direto/{idx}",
            "playback": PlaybackType.WEBVIEW,
            "skill_icon": self.skill_icon,
            "bg_image": ch["img"],
            "skill_id": self.skill_id,
            "javascript": self.javascript,  # webview can run javascript on page load
        } for idx, ch in channels.items()]


def create_skill():
    return RTPSkill()