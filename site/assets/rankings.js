// switches the rankings table between time controls and lists, data from /data/rankings.json
(function () {
  const body = document.getElementById('rank-body');
  const note = document.getElementById('rank-note');
  if (!body) return;
  const LIST_NAMES = { open: 'Open', women: 'Women', juniors: 'Juniors', girls: 'Girls', india: 'India' };
  const CONTROL_NAMES = { standard: 'Standard', rapid: 'Rapid', blitz: 'Blitz' };
  const state = { control: 'standard', list: 'open' };
  let data = null;

  // the choice lives in the address so a link opens the same table
  const params = new URLSearchParams(location.search);
  if (CONTROL_NAMES[params.get('tc')]) state.control = params.get('tc');
  if (LIST_NAMES[params.get('list')]) state.list = params.get('list');

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined && text !== null) n.textContent = text;
    return n;
  };

  function move(r) {
    if (r.was === null || r.was === undefined) return null;
    if (r.was === 0) return el('span', 'mv mv-new', 'new');
    const d = r.was - r.rank;
    if (d === 0) return el('span', 'mv', '–');
    return el('span', d > 0 ? 'mv mv-up' : 'mv mv-down', (d > 0 ? '▲' : '▼') + Math.abs(d));
  }

  function render() {
    const rows = data.lists[state.control][state.list];
    const showMove = rows.some(r => r.was !== null && r.was !== undefined);
    document.querySelectorAll('[data-col="move"]').forEach(n => { n.hidden = !showMove; });
    body.replaceChildren(...rows.map(r => {
      const tr = el('tr');
      tr.append(el('td', 'pos mono', r.rank));
      const mv = el('td', 'mono');
      mv.dataset.col = 'move';
      mv.hidden = !showMove;
      const m = move(r);
      if (m) mv.append(m);
      tr.append(mv);
      const who = el('td', 'who');
      if (r.title) who.append(el('span', 'ttl', r.title));
      const a = el('a', 'dlink', r.name);
      a.href = 'https://ratings.fide.com/profile/' + r.id;
      a.rel = 'noopener';
      a.target = '_blank';
      who.append(a);
      tr.append(who);
      tr.append(el('td', 'fed mono', r.fed));
      tr.append(el('td', 'num mono pts', r.rating));
      tr.append(el('td', 'num mono dim', r.games || '–'));
      tr.append(el('td', 'num mono dim', r.born || '–'));
      return tr;
    }));
    note.textContent = CONTROL_NAMES[state.control] + ' · ' + LIST_NAMES[state.list] +
      ' · FIDE rating list, ' + data.period + ' · active players only';
    document.querySelectorAll('[data-tc]').forEach(b => {
      const on = b.dataset.tc === state.control;
      b.classList.toggle('on', on);
      b.setAttribute('aria-pressed', on);
    });
    document.querySelectorAll('[data-list]').forEach(b => {
      const on = b.dataset.list === state.list;
      b.classList.toggle('on', on);
      b.setAttribute('aria-pressed', on);
    });
  }

  function pick(key, value) {
    state[key] = value;
    const q = new URLSearchParams();
    if (state.control !== 'standard') q.set('tc', state.control);
    if (state.list !== 'open') q.set('list', state.list);
    history.replaceState(null, '', location.pathname + (q.toString() ? '?' + q : ''));
    render();
  }

  document.querySelectorAll('[data-tc]').forEach(b => b.addEventListener('click', () => pick('control', b.dataset.tc)));
  document.querySelectorAll('[data-list]').forEach(b => b.addEventListener('click', () => pick('list', b.dataset.list)));

  fetch('/data/rankings.json')
    .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(d => { data = d; render(); })
    .catch(() => { note.textContent = "Couldn't load the latest list, showing the standard open list from the last build."; });
})();
