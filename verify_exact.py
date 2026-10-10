"""Exact rational feasibility witnesses for unit squares (not optimality proofs).

The checker uses Fraction corner projections, no trigonometry, NumPy, search
geometry, or tolerances. A rational half-angle t yields exactly orthonormal
axes ((1-t*t)/(1+t*t), 2*t/(1+t*t)). This validates the rational witness, which
differs slightly from its numerical parent. It does not formally verify Python.
"""
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path


def check(certificate):
    try:
        if certificate['coordinate_system']!='centered' or certificate['n']!=len(certificate['squares']) or certificate['n']<1:
            raise ValueError('Invalid coordinate system/count')
        L=F(certificate['side']);half=L/2
        if L<=0:raise ValueError('Nonpositive side')
        shapes=[];minimum_wall=None;minimum_pair=None;separators=[]
        for row in certificate['squares']:
            x,y,t=(F(row[k]) for k in ('x','y','t'))
            c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
            axes=((c,s),(-s,c))
            corners=[(x+(a*c-b*s)/2,y+(a*s+b*c)/2) for a,b in ((-1,-1),(1,-1),(1,1),(-1,1))]
            wall=min(half-abs(v) for point in corners for v in point)
            if wall<0:return dict(valid=False,reason='outside wall',square=len(shapes))
            minimum_wall=wall if minimum_wall is None else min(wall,minimum_wall)
            shapes.append((corners,axes))
        for i,(a,aa) in enumerate(shapes):
            for j,(b,bb) in enumerate(shapes[:i]):
                gaps=[]
                for ux,uy in aa+bb:
                    pa=[x*ux+y*uy for x,y in a];pb=[x*ux+y*uy for x,y in b]
                    gaps.append(max(min(pa)-max(pb),min(pb)-max(pa)))
                gap=max(gaps)
                if gap<0:return dict(valid=False,reason='interior overlap',pair=[j,i])
                minimum_pair=gap if minimum_pair is None else min(gap,minimum_pair)
                separators.append([j,i,gaps.index(gap)])
        return dict(valid=True,method='exact rational corners and separating axes',
                    side=str(L),pair_count=len(separators),separators=separators,
                    minimum_wall_gap=str(minimum_wall),minimum_pair_gap=str(minimum_pair) if minimum_pair is not None else None)
    except (KeyError,TypeError,ValueError,ZeroDivisionError,OverflowError) as e:
        return dict(valid=False,reason=str(e))


def rationalize(document,digits=16,dilation='1e-12'):
    """Construct then CHECK; dilation is never treated as an assumed guarantee."""
    if digits<1 or digits>30:raise ValueError('Use 1..30 rationalization digits')
    scale=F(1)+F(dilation)
    if scale<1:raise ValueError('Dilation must be nonnegative')
    def rational(v):return F(format(float(v),f'.{digits}f'))
    rows=[]
    for x,y,theta in document['poses']:
        theta=(float(theta)+math.pi/4)%(math.pi/2)-math.pi/4
        rows.append(dict(x=str(rational(x)*scale),y=str(rational(y)*scale),t=str(rational(math.tan(theta/2)))))
    cert=dict(schema='sqpack-rational-v1',n=len(rows),coordinate_system='centered',
              side=str(F(repr(float(document['side'])))*scale),squares=rows,
              parent_side=repr(float(document['side'])),dilation=str(F(dilation)))
    report=check(cert)
    if not report['valid']:raise ValueError(f'Rationalized packing failed exact verification: {report}')
    return cert,report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source');parser.add_argument('--out');parser.add_argument('--check',action='store_true')
    parser.add_argument('--dilation',default='1e-12');args=parser.parse_args()
    data=json.loads(Path(args.source).read_text())
    if args.check:report=check(data)
    else:
        cert,report=rationalize(data.get('best',data),dilation=args.dilation)
        if not args.out:parser.error('--out is required to save the exact witness')
        Path(args.out).write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='separators'},indent=2))
    if not report['valid']:raise SystemExit(1)


if __name__=='__main__':main()
