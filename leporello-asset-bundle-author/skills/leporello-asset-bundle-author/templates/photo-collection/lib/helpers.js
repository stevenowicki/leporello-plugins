/*
 * Leporello v1 DLS — bundle runtime helpers.
 *
 * Pure runtime utilities, no framework dependencies. Every restyled template
 * includes this verbatim (or inlines what it needs). Implements the M1
 * direction's stage + background-media + roster mechanics
 * (docs/prelim/dls/m1/direction/direction.md).
 *
 * Public API (global `leporello`):
 *   - fitStage(selector?)                  scale a 1920x1080 stage to viewport
 *   - mountBackgroundMedia(opts)           mount an ambient image OR video + scrim
 *   - renderRoster(container, rows, opts?) build proportional roster bars (§5.13)
 *   - loadContent(path?)                   fetch JSON content (default ./content.json)
 *   - loadManifest()                       fetch ./manifest.json
 *   - applyVersionStamp(manifest, root?)   stamp data-version / data-updated
 */

(function (global) {
	const leporello = {};

	const STAGE_W = 1920;
	const STAGE_H = 1080;

	/* -----------------------------------------------------------------
	 * fitStage(selector?)
	 * Scales the fixed-size 1920x1080 stage to fit the viewport (contain),
	 * preserving aspect ratio. Re-fits on resize. The stage is authored at
	 * native px; everything downstream of it inherits the scale.
	 *
	 *   selector — CSS selector for the stage element. Default '.lep-stage'.
	 * --------------------------------------------------------------- */
	leporello.fitStage = function fitStage(selector) {
		const stage = document.querySelector(selector || '.lep-stage');
		if (!stage) return;

		function fit() {
			const s = Math.min(
				window.innerWidth / STAGE_W,
				window.innerHeight / STAGE_H
			);
			stage.style.transform = 'scale(' + s + ')';
		}
		fit();
		window.addEventListener('resize', fit);
	};

	/* -----------------------------------------------------------------
	 * mountBackgroundMedia(opts)
	 * Mounts the full-bleed ambient background-media layer (image OR video)
	 * with the MANDATORY legibility scrim (direction §4 + §5.4). The layer is
	 * inserted as the first child of the stage so it sits behind all content.
	 *
	 *   opts.stage    — stage element or selector. Default '.lep-stage'.
	 *   opts.image    — image URL (mutually exclusive with .video).
	 *   opts.video    — video URL. Mounted muted/looping/autoplay/playsinline,
	 *                   low-motion ambient per §5.4. Keep loops short + compressed.
	 *   opts.poster   — poster image for the video (shown before/while loading).
	 *   opts.scrim    — 'default' | 'heavy' | 'left'. Default 'default'.
	 *                   All stay within the §5.4 rgba(10,14,20,0.55-0.78) mandate.
	 *
	 * Returns the layer element (or null if nothing to mount).
	 * --------------------------------------------------------------- */
	leporello.mountBackgroundMedia = function mountBackgroundMedia(opts) {
		opts = opts || {};
		const stage =
			typeof opts.stage === 'string'
				? document.querySelector(opts.stage)
				: opts.stage || document.querySelector('.lep-stage');
		if (!stage) return null;
		if (!opts.image && !opts.video) return null;

		const layer = document.createElement('div');
		layer.className = 'lep-bg-media';

		if (opts.video) {
			const v = document.createElement('video');
			v.src = opts.video;
			v.muted = true;
			v.loop = true;
			v.autoplay = true;
			v.playsInline = true;
			v.setAttribute('playsinline', '');
			v.setAttribute('muted', '');
			if (opts.poster) v.poster = opts.poster;
			// Best-effort autoplay; harmless if blocked (capture sees first frame).
			const p = v.play();
			if (p && typeof p.catch === 'function') p.catch(function () {});
			layer.appendChild(v);
		} else {
			const img = document.createElement('img');
			img.src = opts.image;
			img.alt = '';
			layer.appendChild(img);
		}

		const scrim = document.createElement('div');
		scrim.className = 'lep-bg-scrim';
		if (opts.scrim === 'heavy') scrim.classList.add('lep-bg-scrim--heavy');
		else if (opts.scrim === 'left') scrim.classList.add('lep-bg-scrim--left');
		layer.appendChild(scrim);

		stage.insertBefore(layer, stage.firstChild);
		return layer;
	};

	/* -----------------------------------------------------------------
	 * renderRoster(container, rows, opts?)
	 * Builds a roster where each row carries a proportional bar sized to its
	 * metric, leader longest (direction §5.13 — "rosters encode their metric").
	 * The eye gets the ranking from bar length before reading any digit; the
	 * value stays the hero (largest, tabular).
	 *
	 *   container — element or selector to render into.
	 *   rows      — array of { label, value, display? }.
	 *                 value: number used for bar proportion + default display.
	 *                 display: optional preformatted string for the value cell
	 *                          (e.g. "62%", "1,284"). Falls back to value.
	 *   opts.sort       — sort descending by value before render. Default true.
	 *   opts.max        — bar-scale denominator. Default = max row value.
	 *   opts.leaderIndex— index (post-sort) to paint with data-accent. Default 0.
	 *                     Pass null to color every bar data-primary.
	 *   opts.onBar      — when true, the LABEL rides inside the bar (over the
	 *                     fill) instead of above it. The label gets the on-bar
	 *                     halo (.lep-on-bar) so it stays legible when the bar is
	 *                     short and the name overflows onto the dark track
	 *                     (direction §5.13). Default false (label above bar).
	 *
	 * Returns the array of row elements created.
	 * --------------------------------------------------------------- */
	leporello.renderRoster = function renderRoster(container, rows, opts) {
		opts = opts || {};
		const el =
			typeof container === 'string'
				? document.querySelector(container)
				: container;
		if (!el || !Array.isArray(rows) || rows.length === 0) return [];

		let data = rows.slice();
		if (opts.sort !== false) {
			data.sort(function (a, b) {
				return (b.value || 0) - (a.value || 0);
			});
		}
		const max =
			opts.max != null
				? opts.max
				: data.reduce(function (m, r) {
						return Math.max(m, r.value || 0);
				  }, 0) || 1;
		const leaderIndex = opts.leaderIndex === undefined ? 0 : opts.leaderIndex;
		const onBar = opts.onBar === true;

		el.classList.add('lep-roster');
		el.classList.toggle('lep-roster--on-bar', onBar);
		el.innerHTML = '';
		const created = [];

		data.forEach(function (r, i) {
			const row = document.createElement('div');
			row.className = 'lep-roster-row';

			const label = document.createElement('div');
			label.className = 'lep-roster-label';
			// On-bar labels overflow onto the dark track when the bar is short,
			// so they carry the on-bar halo to stay legible (direction §5.13).
			if (onBar) label.classList.add('lep-on-bar');
			label.textContent = r.label != null ? r.label : '';

			const value = document.createElement('div');
			value.className = 'lep-roster-value';
			value.textContent = r.display != null ? r.display : String(r.value);

			const barWrap = document.createElement('div');
			barWrap.className = 'lep-roster-bar-wrap';
			const bar = document.createElement('div');
			bar.className = 'lep-roster-bar';
			if (leaderIndex != null && i === leaderIndex) {
				bar.classList.add('lep-roster-bar--leader');
			}
			const pct = Math.max(0, Math.min(100, ((r.value || 0) / max) * 100));
			bar.style.width = pct + '%';
			barWrap.appendChild(bar);

			if (onBar) {
				// Label sits inside the bar wrap, over the fill.
				barWrap.appendChild(label);
				row.appendChild(value);
				row.appendChild(barWrap);
			} else {
				row.appendChild(label);
				row.appendChild(value);
				row.appendChild(barWrap);
			}
			el.appendChild(row);
			created.push(row);
		});

		return created;
	};

	/* -----------------------------------------------------------------
	 * Content / manifest plumbing (carried from the foundation lib).
	 * --------------------------------------------------------------- */
	leporello.loadContent = async function loadContent(path) {
		const url = path || './content.json';
		const r = await fetch(url, { cache: 'no-store' });
		if (!r.ok) throw new Error('Failed to load ' + url + ': ' + r.status);
		return r.json();
	};

	leporello.loadManifest = async function loadManifest() {
		const r = await fetch('./manifest.json', { cache: 'no-store' });
		if (!r.ok) throw new Error('Failed to load manifest.json: ' + r.status);
		return r.json();
	};

	leporello.applyVersionStamp = function applyVersionStamp(manifest, root) {
		const el = root || document.documentElement;
		if (manifest.version != null) {
			el.setAttribute('data-version', String(manifest.version));
		}
		if (manifest.editorialReview && manifest.editorialReview.reviewedAt) {
			el.setAttribute('data-updated', manifest.editorialReview.reviewedAt);
		} else if (manifest.createdAt) {
			el.setAttribute('data-updated', manifest.createdAt);
		}
	};

	global.leporello = leporello;
})(window);
