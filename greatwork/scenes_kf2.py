import sys, concurrent.futures as cf
from img import edit, STYLE
REFS=['keyframes/ref_style.png','keyframes/ref_explorer.png']
PRE="Use the attached reference images: match the exact art style, palette and lighting of the style sheet, and the exact Explorer character (teal hooded coat, satchel, faceless dark round head, amber lantern) from the character sheet. "+STYLE+" Keep the upper fifth of the frame calm and uncluttered. "
K={
'1b_lantern':"Scene: extreme close-up of the Explorer's gloved hand holding the glowing amber lantern at dusk, blurred sea and low sun glow behind, teal coat sleeve in frame.",
'1c_dock':"Scene: the Explorer seen from behind walking along a rocky shore at dusk toward a small moored wooden sailboat with a furled cream sail, lantern in hand, calm water, low amber sun.",
'2a_board':"Scene: the Explorer stepping into the small wooden sailboat (same boat as the style sheet) at the rocky shore, lantern held up, one foot on the boat, sail beginning to unfurl, dusk light.",
'2c_tiller':"Scene: medium close shot of the Explorer seated at the stern of the sailboat with a hand on the wooden tiller, the lantern glowing beside, starry navy sky, dark water.",
'2d_tack':"Scene: the sailboat heeling over on a tack across dark water, the boom swinging across, white spray at the bow, the Explorer leaning into the turn with the lantern, dynamic angle.",
'2e_dawn':"Scene: the sailboat on a wide calm sea at first dawn light sailing toward a distant dark mountain, a long zigzag wake trail behind it, sky turning amber and teal, high wide shot.",
'3a_landing':"Scene: the sailboat moored at a rocky shore at dawn, the Explorer stepping onto the rocks and looking up at a tall dark mountain towering ahead, lantern in hand.",
'4a_edge':"Scene: the Explorer at the jagged edge of the mountain, lantern raised, small thin cracks across the rock face beginning to glow faint teal, dramatic dark mountain.",
'4b_touch':"Scene: close view of the Explorer's gloved hand pressed on the rock face, glowing teal veins spreading across the stone around the hand, dust particles in the lantern light.",
'4d_world':"Scene: view through a narrow opened crack in a dark rock face into a hidden luminous world: glowing waterfalls, teal bridges, floating amber lights; the Explorer's dark silhouette in the foreground edge of the frame.",
'5a_raft':"Scene: a tiny rough raft of a few lashed planks and a stick mast with a scrap of cloth, on a sandy shore at dusk with calm sea, simple flat vector, no character.",
'5b_boat':"Scene: a small neat wooden sailboat with one cream sail on the same sandy shore at dusk with calm sea, same composition and camera angle as the raft shot, no character.",
'5c_ship':"Scene: a large handsome wooden sailing ship with three cream sails on calm sea at dusk, amber lantern glow at the stern, same composition and horizon line, no character.",
'6b_cross':"Scene: the Explorer seen from behind in the middle of the thin glowing teal bridge, mist swirling in the dark chasm below, a bright sunlit peak ahead, lantern held out.",
'6c_peak':"Scene: the Explorer small at the far end of the bridge on a ledge, looking up at the highest mountain peak lit by sunrise, golden light on the snow.",
'7a_camp':"Scene: night on a high mountain ridge, the Explorer sitting by the glowing amber lantern with knees up, stars filling the navy sky, calm and warm.",
'7b_storm':"Scene: a fierce gust of wind and snow on a night ridge, the Explorer hunched cupping the lantern with both hands, the flame small and nearly out, streaks of snow blowing.",
'7c_lanterns':"Scene: night mountain ridge with many small glowing amber lanterns dotted along the ridge and the slopes below (other travellers), the Explorer in the foreground with a bright rekindled lantern, stars above.",
'8b_summit':"Scene: wide view from the summit over misty valleys and layered mountain ranges at sunrise, golden light spreading, a glowing bud of light on the horizon, no character in frame.",
'8c_doubt':"Scene: the Explorer at the summit edge seen from the side with the lantern lowered, looking out at the vast glowing horizon, a hint of hesitation in the posture.",
'8d_bud':"Scene: the Explorer at the summit from behind, lantern raised high, the glowing bud of light on the horizon wide open like a lotus with radiating golden and teal rays over the mountains.",
}
only=sys.argv[1:] or list(K)
with cf.ThreadPoolExecutor(4) as ex:
    list(ex.map(lambda k: edit(k,PRE+K[k],REFS),only))
