:- [pairs_kb].
edge(X, Y, Weight) :- arc(X, Y, Weight) ; arc(Y, X, Weight).

path([Begin], End, [Begin], Cost) :- edge(Begin, End, Cost).
path(Visited, End, [Last | Path1], Cost) :-
    member(Last, Visited),
    delete(Visited, Last, Visited1),
    min_path(Visited1, Last, Path1, Cost1),
    edge(Last, End, Cost0),
    Cost is Cost0+Cost1.

min_path(Visited, End, Path, Cost) :-
    path(Visited, End, Path, Cost),
    \+ (path(Visited, End, _, T), T<Cost).

hami_cycle(Start, Nodes,[Start | Path], Cost) :-
    min_path(Nodes, Start, Path, Cost1),
    last(Path, Last),
    edge(Start, Last, Cost0),
    Cost is Cost0+Cost1.

travel(Start, Nodes,Path, Cost) :-
    hami_cycle(Start,Nodes,Path, Cost),
    \+ (hami_cycle(Start,Nodes,_, T), T<Cost).
