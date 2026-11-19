from streamlink.plugins.pluto import Pluto, PlutoHLSSegment, PlutoM3U8Parser
from streamlink.stream.hls import parse_m3u8
from tests.plugins import PluginCanHandleUrl


class TestPluginCanHandleUrlPluto(PluginCanHandleUrl):
    __plugin__ = Pluto

    should_match_groups = [
        (
            (
                "live",
                "https://pluto.tv/en/live-tv/61409f8d6feb30000766b675",
            ),
            {
                "id": "61409f8d6feb30000766b675",
            },
        ),
        (
            (
                "series",
                "https://pluto.tv/en/on-demand/series/5e00cd538e67b0dcb2cf3bcd/season/1/episode/60dee91cfc802600134b886d",
            ),
            {
                "id_s": "5e00cd538e67b0dcb2cf3bcd",
                "id_e": "60dee91cfc802600134b886d",
            },
        ),
        (
            (
                "movies",
                "https://pluto.tv/en/on-demand/movies/5ed28c8cefbd62001b280de6",
            ),
            {
                "id": "5ed28c8cefbd62001b280de6",
            },
        ),
        (
            (
                "series",
                "https://pluto.tv/gsa/shows/2740225/episode/60dee91cfc802600134b886d/",
            ),
            {
                "id_s": "2740225",
                "id_e": "60dee91cfc802600134b886d",
            },
        ),
        (
            (
                "movies",
                "https://pluto.tv/us/movies/6925771d1a8e9be91b1b7d22/#open",
            ),
            {
                "id": "6925771d1a8e9be91b1b7d22",
            },
        ),
        (
            (
                "live",
                "https://pluto.tv/fr/watch/live-tv/31528/",
            ),
            {
                "id": "31528",
            },
        ),
    ]

    should_not_match = [
        "https://pluto.tv/live-tv",
    ]


class TestPlutoM3U8Parser:
    # regression: the EXT-X-DISCONTINUITY-SEQUENCE tag is inherited from the base parser's
    # tag registry, so a broken tag registration there breaks the plugin subclass as well
    def test_discontinuity_sequence_inherited(self):
        data = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:6
#EXT-X-DISCONTINUITY-SEQUENCE:5
#EXTINF:2.000,
segment0.ts
#EXT-X-ENDLIST
"""
        playlist = parse_m3u8(data, "http://test.se/", parser=PlutoM3U8Parser)

        assert isinstance(playlist.discontinuity_sequence, int)
        assert playlist.discontinuity_sequence == 5
        assert type(playlist.segments[0]) is PlutoHLSSegment
