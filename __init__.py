from ovos_plugin_common_play.ocp import MediaType, PlaybackType
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, ocp_search, ocp_featured_media


class RTPSkill(OVOSCommonPlaybackSkill):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.supported_media = [MediaType.TV, MediaType.GENERIC]
        self.skill_icon = self.default_bg = "https://cdn-images.rtp.pt/common/img/channels/logos/gray-negative/horizontal/rtp.png"
        self.channels = {
            "rtp1": {
                "name": "RTP1",
                "img": "5-563718101410.png"
            },
            "rtp2": {
                "name": "RTP2",
                "img": "3-363718101410.png"
            },
            "rtp3": {
                "name": "RTP3",
                "img": "64-393818101410.png"
            },
            "rtpinternacional": {
                "name": "RTP Internacional",
                "img": "120-344318101410.png"
            },
            "rtpmemoria": {
                "name": "RTP Memoria",
                "img": "80-584819141705.png"
            },
            "rtpmadeira": {
                "name": "RTP Madeira",
                "img": "107-443519141305.png"
            },
            "rtpacores": {
                "name": "RTP Açores",
                "img": "106-563419141305.png"
            },
            "rtpafrica": {
                "name": "RTP Africa",
                "img": "27-363219141305.png"
            }
        }

    @property
    def javascript(self):
        # webview can run javascript on page load
        # useFullscreen is provided by OCP, it will
        # - find a video element
        # - remove all other elements
        # - toggle fullscreen
        # TODO RTP video player starts muted, figure out how to unmute
        return """useFullscreen()"""

    @ocp_featured_media()
    def featured_media(self):
        return [
            {
                "title": ch["name"],
                "image":
                f'https://cdn-images.rtp.pt/common/img/channels/logos/color/horizontal/{ch["img"]}',
                "match_confidence": 80,
                "media_type": MediaType.TV,
                "uri": f"https://www.rtp.pt/play/direto/{idx}",
                "playback": PlaybackType.WEBVIEW,
                "skill_icon": self.skill_icon,
                "bg_image":
                f'https://cdn-images.rtp.pt/common/img/channels/logos/color/horizontal/{ch["img"]}',
                "skill_id": self.skill_id,
                "javascript":
                self.javascript,  # webview can run javascript on page load
            } for idx, ch in self.channels.items()
        ]

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

    @ocp_search()
    def search_db(self, phrase, media_type):
        if self.voc_match(phrase, "rtp"):
            score = self.match_skill(phrase, media_type)
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
