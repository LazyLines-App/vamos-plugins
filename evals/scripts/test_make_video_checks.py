"""make-video's code checks, on synthetic files made here with ffmpeg (nothing binary in git, no network).

    python3 evals/scripts/test_make_video_checks.py

Each test is a way a finished video failed its maker in the 11-12 trial, while the old checks printed PASS:
a blank first frame (the feed's cover), a line whose thing wasn't on screen when it was said, an ending whose
words changed in a fix, captions that broke after "are" and "their", and a take the model re-voiced.
Needs ffmpeg; the beat test needs tesseract and is skipped without it.
"""
import json, os, shutil, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS = os.path.join(ROOT, 'plugins', 'cracked-marketer', 'skills', 'make-video', 'scripts')
sys.path.insert(0, SCRIPTS)
import captions  # noqa: E402
import checklib  # noqa: E402


def ff(*args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args], check=True)


def save(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)


def words(text, start=0.25, each=0.3):
    out, t = [], start
    for w in text.split():
        out.append({'word': w, 'start': round(t, 2), 'end': round(t + each - 0.05, 2)})
        t += each
    return out


def check_video(video, *args):
    p = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'check-video.py'), video, '--format', 'other', *args],
                       capture_output=True, text=True)
    return p.stdout + p.stderr


class MakeVideoChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp(prefix='mv-checks-')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, ignore_errors=True)

    def path(self, name):
        return os.path.join(self.dir, name)

    def test_blank_cover_fails(self):
        """Frame 0 is the cover in the feed: a white frame fading into the first scene fails; a scene drawn whole passes."""
        scene = self.path('scene.mp4')
        ff('-f', 'lavfi', '-i', 'testsrc2=s=1080x1920:r=30:d=3', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
           '-t', '3', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', scene)
        faded = self.path('faded.mp4')
        ff('-i', scene, '-vf', 'fade=in:st=0:d=0.6:color=white', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'copy', faded)
        self.assertIn('DEFECT frame 0', check_video(faded))
        self.assertNotIn('DEFECT frame 0', check_video(scene))
        # a typed ask on a flat colour is a cover too, even when a busy screen lands right after it
        typed = self.path('typed.mp4')
        ff('-i', scene, '-vf', "drawbox=c=white:t=fill:enable='lt(t,0.4)',"
           "drawtext=text='Find me hooks beating their usual':fontsize=44:x=120:y=900:fontcolor=black:enable='lt(t,0.4)'",
           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'copy', typed)
        self.assertNotIn('DEFECT frame 0', check_video(typed))

    @unittest.skipUnless(shutil.which('tesseract'), 'tesseract not installed')
    def test_payoff_off_screen_fails(self):
        """'then writes yours' must play over the written hook, not over the chat while it loads."""
        video = self.path('beats.mp4')
        ff('-f', 'lavfi', '-i', 'color=white:s=1080x1920:r=30:d=4', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
           '-t', '4', '-vf',
           "drawtext=text='Thinking':fontsize=110:x=(w-tw)/2:y=700:fontcolor=black:enable='lt(t,2)',"
           "drawtext=text='Stop guessing hooks':fontsize=110:x=(w-tw)/2:y=700:fontcolor=black:enable='gte(t,2)'",
           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', video)
        beats = self.path('beats.json')
        save(beats, [{'line': 'then writes yours.', 'shows': 'Stop guessing hooks'}])
        early, late = self.path('early.json'), self.path('late.json')
        save(early, words('then writes yours.', start=0.4))  # "yours" at about 1.0 s
        save(late, words('then writes yours.', start=2.2))   # "yours" at about 2.8 s
        out = check_video(video, '--words', early, '--beats', beats)
        self.assertIn('DEFECT beat 1', out)
        self.assertNotIn('DEFECT beat', check_video(video, '--words', late, '--beats', beats))
        # a cover row needs no line
        save(beats, [{'t': 0, 'shows': 'Thinking'}])
        self.assertNotIn('DEFECT beat', check_video(video, '--words', late, '--beats', beats))

    @unittest.skipUnless(shutil.which('tesseract'), 'tesseract not installed')
    def test_caption_never_proves_a_beat(self):
        """A line that quotes the screen: the caption saying the words doesn't count as the screen showing them."""
        cues = [{'text': 'Stop washing', 'start': 0.0, 'end': 0.85}, {'text': 'your face twice a day.', 'start': 0.85, 'end': 3.0}]
        caption = ("drawtext=text='Stop washing':fontsize=64:x=(w-tw)/2:y=1300:fontcolor=black:enable='lt(t,0.85)',"
                   "drawtext=text='your face twice a day.':fontsize=64:x=(w-tw)/2:y=1300:fontcolor=black:enable='gte(t,0.85)'")
        save(self.path('q-cues.json'), cues)
        save(self.path('q-words.json'), words('Stop washing your face twice a day.', start=0.25))
        save(self.path('q-beats.json'), [{'line': 'Stop washing your face twice a day.', 'shows': 'Stop washing your face twice a day'}])
        for name, screen, want in (('loading', 'Thinking', True), ('quote', 'STOP WASHING YOUR FACE TWICE A DAY', False)):
            video = self.path(f'q-{name}.mp4')
            ff('-f', 'lavfi', '-i', 'color=white:s=1080x1920:r=30:d=3', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
               '-t', '3', '-vf', f"drawtext=text='{screen}':fontsize=56:x=(w-tw)/2:y=600:fontcolor=black,{caption}",
               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', video)
            out = check_video(video, '--words', self.path('q-words.json'), '--captions', self.path('q-cues.json'),
                              '--beats', self.path('q-beats.json'))
            self.assertEqual('DEFECT beat 1' in out, want, out)

    def test_changed_ending_fails(self):
        """A fix that turns 'and I'll send you the setup' into 'and do the setup' is caught; '20' heard as 'twenty' is not."""
        script = "Comment HOOKS and I'll send you the setup."
        diff = checklib.word_diff(script, words('Comment hooks and do the setup'))
        self.assertTrue(any(k == 'DEFECT' and 'send' in said for k, said, heard, t in diff), diff)
        self.assertEqual(checklib.word_diff('that did 20 or 30 times', words('that did twenty or thirty times')), [])
        # a brand name the transcriber always mishears, in the clean read too, is a FLAG, not a DEFECT
        read = words('Ask Famos for the hooks')
        diff = checklib.word_diff('Ask Vamos for the hooks', words('Ask Famos for the hooks'), read)
        self.assertEqual([k for k, *_ in diff], ['FLAG'])

    def test_captions_break_at_phrases(self):
        """No caption ends on a word that needs the next one ('are', 'their', 'can', 'the')."""
        text = ("Most hooks you scroll past are guesses. The ones that work can be measured. Vamos compares each "
                "video's views with its creator's usual, and finds the videos in your niche that did twenty or "
                "thirty times their creator's usual.")
        out = captions.cues(captions.phrases(captions.display_words(words(text), text)))
        for q in out:
            last = q['text'].split()[-1]
            self.assertFalse(captions.bare(last) in captions.NEEDS_NEXT and not captions.ends_phrase(last), q['text'])
            self.assertLessEqual(len(q['text'].split()), 6)
        said = ' '.join(q['text'] for q in out)
        self.assertEqual(said, text)  # every word, in order, as the script writes it
        # over a demo (3 words a caption), a phrase with no good break runs long rather than end on "it's" or "a"
        for q in captions.cues(captions.phrases(captions.display_words(words(text), text), max_words=3)):
            last = q['text'].split()[-1]
            self.assertFalse(captions.bare(last) in captions.NEEDS_NEXT and not captions.ends_phrase(last), q['text'])
        # a pause after a little word ("her ... usual") is not a place to break
        w = words('This skincare hook did thirty times her usual.')
        for x in w[-1:]:
            x['start'] += 0.5
            x['end'] += 0.5
        self.assertNotIn('did thirty times her', [q['text'] for q in captions.cues(captions.phrases(w))])
        # a brand the transcriber mishears is captioned as the script spells it
        shown = captions.display_words(words('Podly finds your best posts'), 'Potly finds your best posts.')
        self.assertEqual(shown[0]['word'], 'Potly')
        # and check-video fails captions that break by count
        video = self.path('cap.mp4')
        ff('-f', 'lavfi', '-i', 'testsrc2=s=1080x1920:r=30:d=5', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
           '-t', '5', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', video)
        w = words('Most hooks you scroll past are guesses.')
        bad = [{'text': 'Most hooks you scroll past are', 'start': 0.1, 'end': 1.9},
               {'text': 'guesses.', 'start': 1.9, 'end': 2.6}]
        wj, cj = self.path('w.json'), self.path('bad.json')
        save(wj, w)
        save(cj, bad)
        self.assertIn('DEFECT', check_video(video, '--words', wj, '--captions', cj))

    def test_revoiced_take_fails(self):
        """A take whose sound is no longer the read it was given (the model re-voiced it) scores under 0.9."""
        def voice(name, period, d=4):
            out = self.path(name)
            ff('-f', 'lavfi', '-i', f'sine=f=220:d={d}', '-af',
               f"volume='if(lt(mod(t,{period}),{period / 2}),1,0.03)':eval=frame", '-ar', '48000', out)
            return out
        read = voice('read.wav', 0.6)
        black = self.path('voice-video.mp4')
        ff('-f', 'lavfi', '-i', 'color=black:s=480x854:r=24:d=4', '-i', read, '-shortest', '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p', '-c:a', 'aac', black)
        kept = self.path('kept.mp4')
        ff('-f', 'lavfi', '-i', 'testsrc2=s=480x854:r=24:d=4', '-i', read, '-shortest', '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p', '-c:a', 'aac', kept)
        revoiced = self.path('revoiced.mp4')
        ff('-f', 'lavfi', '-i', 'testsrc2=s=480x854:r=24:d=4', '-i', voice('other.wav', 0.5), '-shortest',
           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', revoiced)
        self.assertGreaterEqual(checklib.envelope_match(kept, black), 0.9)
        self.assertLess(checklib.envelope_match(revoiced, black), 0.9)
        p = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'check-take.py'), revoiced, '--voice', black],
                           capture_output=True, text=True)
        self.assertIn('DEFECT re-voiced', p.stdout)
        self.assertEqual(p.returncode, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
