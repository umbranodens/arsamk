# Responsive illustrations

Sources stay in `assets/img/`: `hero.png`, `cara-kerja.png`, and `porto.png`.
The page loads only the WebP variants in this directory.

Each illustration has widths of 480, 768, 1200, and its original width
(1672 for hero, 1671 for the others). Aspect ratios are preserved; there is
no crop or upscale. Encoded with Sharp, WebP quality 84 and effort 6,
auto-orientation enabled, and metadata stripped by the encoder.

`index.html` defines `srcset`, layout-specific `sizes`, and intrinsic
width/height. Hero loads eagerly with high priority. Process and portfolio
load lazily. All three are decorative (`alt=""`); the adjacent text carries
the content, and the portfolio caption identifies the illustration.

Keep the original compositions visible when changing the layout. In
particular, avoid `object-fit: cover`, grayscale filters, and duplicating
the red shapes already present in the supplied artwork.
