# Responsive illustrations

The page loads responsive WebP assets with srcset, layout-specific sizes,
and intrinsic width/height. Images preserve their original aspect ratio
without cropping or upscaling. The hero loads eagerly with high priority;
process and portfolio images load lazily and decode asynchronously.
Images are decorative (alt=""); adjacent text provides the content.

## Portfolio exhibit

Source: ../Architectural exhibit with red display screens.png (1536 x 1024).
The original PNG is retained unchanged. portfolio-exhibit-{480,768,1200,1536}.webp
are encoded using cwebp 1.6.0, quality 84, method 6, sharp YUV conversion,
and no metadata. The source is opaque; its original colors are retained.
No CSS color filter or blend mode is applied to the new portfolio image.
The largest variant supports approximately 2x density at its desktop size.

## Existing illustrations

hero-*.webp and cara-kerja-*.webp use widths 480, 768, 1200, and their
original widths (1672 for hero, 1671 for process), preserving aspect ratio.
These were encoded using Sharp with WebP quality 84 and effort 6,
auto-orientation enabled, and metadata stripped.

porto-*.webp are earlier portfolio assets retained for the previous layout;
they are no longer referenced by index.html.

## Contact brainstorming

Source: ../Pencil brainstorming with a giant red bulb.png (1536 x 1024).
contact-brainstorm-{480,768,1200,1536}.webp preserve the full composition
and original transparency. Encoded with cwebp quality 84, method 6, sharp
YUV, alpha quality 100, and no metadata. No upscaling or color filters.
The original PNG is retained unchanged. Contact uses responsive sizes,
explicit dimensions, lazy loading and asynchronous decoding.
