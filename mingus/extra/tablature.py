import mingus.extra.tunings as tunings
import mingus.core.value as value

def begin_track(tuning, padding = 2):
        names = [ x.to_shorthand() for x in tuning.tuning ]
        basesize = len(max(names)) + 3
        res = []
        for x in names:
                r = " %s" % x
                spaces = basesize - len(r)
                r += " " * spaces + "||" + "-" * padding
                res.append(r)
        return res




def from_Note(note, tuning = None):
        if tuning is None:
                tuning = tunings.get_tuning("Guitar", "Standard")

        result = begin_track(tuning)

        # Do an attribute check


        # otherwise:
        min = 1000
        s, f = -1, -1
        for string, fret in enumerate(tuning.find_frets(note)):
                if fret is not None:
                        if fret < min:
                                min = fret
                                s, f = string, fret

        if min != 1000:
                fret = str(f)
                for i in range(len(result)):
                        if i != s:
                                result[i] += "-" * len(fret) + "--|"
                        else:
                                result[i] += fret + "--|"
        else:
                #warning no fret found
                pass
        result.reverse()
        return result


def from_NoteContainer(notes, tuning = None):

        if tuning is None:
                tuning = tunings.get_tuning("Guitar", "Standard")


        result = begin_track(tuning)
        
        fingerings = tuning.find_fingering(notes)

        if fingerings != []:
                res = {}
                f = fingerings[0]
                for string, fret in f:
                        res[string] = str(fret)
                maxfret = max(res.values())

                for i in range(len(result)):
                        if i not in res.keys():
                                result[i] += "-" * len(maxfret) + "--|"
                        else:
                                result[i] += ("%" + str(len(maxfret)) + "s") % res[i] + "--|"

        else:
                #warning no fingerings
                pass

        result.reverse()
        return result


def from_Bar(bar, tuning = None):

        if tuning is None:
                tuning = tunings.get_tuning("Guitar", "Standard")


        qsize = 12
        result = begin_track(tuning, qsize / 2)
        
        for entry in bar.bar:
                beat, duration, notes = entry
                base, dots, rat1, rat2 = value.determine(duration)
                fingering = tuning.find_fingering(notes)
                if fingering != []:
                        f = fingering[0]
                        maxlen = 0
                        d = {}
                        for string, fret in f:
                                d[string] = str(fret)
                                if len(str(fret)) > maxlen:
                                        maxlen = len(str(fret))
                        for i in range(len(result)):
                                dur = int(1.0 / duration * qsize * 4) - maxlen
                                if i not in d.keys():
                                        result[i] += "-" * maxlen + "-" * dur
                                else:
                                        result[i] += ("%" + str(maxlen) + "s") % d[i] + "-" * dur
                else:
                        #warning no fingerings
                        pass
        
        for i in range(len(result)):
                result[i] += "--|"

        result.reverse()
        return result