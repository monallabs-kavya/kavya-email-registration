from twtags_safelist import get_twtags_safelist
from svelte_bundler import build_ssr_style_css

target_module = "td_set_cookie_for_logged_in_user"
build_ssr_style_css(target_module,
                    output_dir="./static/ssr/",
                    )
