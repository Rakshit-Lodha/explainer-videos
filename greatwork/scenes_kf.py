import sys
from img import edit, STYLE, EXPLORER
REFS=['keyframes/ref_style.png','keyframes/ref_explorer.png']
PRE="Use the attached reference images: match the exact art style, palette and lighting of the style sheet, and the exact Explorer character (teal hooded coat, satchel, faceless dark round head, amber lantern) from the character sheet. "+STYLE+" Keep the upper fifth of the frame calm and uncluttered for captions. "
S={
's1':"Scene: the Explorer seen from behind and slightly to the side, standing small on a dark rocky shoreline at dusk, lantern lit in hand, looking out over calm water toward a far glowing horizon with a low amber sun. Wide shot, figure in the lower third.",
's2':"Scene: the Explorer sitting at the stern of a small sailboat (the same sailboat as the style sheet) on calm dark water, lantern glowing brightly and casting amber light across the sail and water, boat heeled slightly as if tacking, distant mountain silhouettes on the horizon.",
's3':"Scene: the Explorer small in the lower third, climbing a rocky mountain slope, lantern raised; the mountain's far edge above is smooth from a distance but its outline near the top breaks into a jagged fractal of repeating angular shards, faint teal light at the tips.",
's4':"Scene: close, dramatic view of the Explorer holding the lantern up to a crack in the mountain edge; teal light pours from several small cracks, one crack pried open revealing a glowing hidden world of amber and teal light inside, light spilling onto the Explorer's coat.",
's6':"Scene: the Explorer walking along a thin glowing teal bridge (like the bridge in the style sheet) from a stable dark ledge on the left toward a bright mountain peak on the right, a deep misty chasm below, lantern flaring brightly, seen from behind, wide composition.",
's8':"Scene: the Explorer standing at the summit seen from behind, lantern raised high; ahead, the horizon is glowing teal and amber with a luminous bud of light opening like a flower above distant mountains, calm hopeful ending frame.",
}
for k in (sys.argv[1:] or S): edit(f'{k}_kf',PRE+S[k],REFS)
