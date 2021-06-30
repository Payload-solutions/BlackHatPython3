{-# LANGUAGE GADTs, UndecidableInstances, InstanceSigs, RankNTypes, TemplateHaskell #-}
module Klytius
where

import qualified Control.Applicative as A hiding (empty)
import qualified Control.Parallel as P
import Language.Haskell.TH.Syntax 


-- | Basic type representing the EDSL.
data TPar s where
    Par' :: TPar a -> TPar s -> TPar s --  Constructor which represents par primitive
    Seq' :: TPar a -> TPar s -> TPar s --  Constructor which represents pseq primitive
    Val' :: s -> TPar s                --  Value inyector? 
    Lbl  :: TLabel -> TPar a -> TPar a --  Label management.

-- | Labels as a pair of strings. Left string for 'dynamic labels' and right string
-- for 'value labels' 
type TLabel = (String, String)

instance Functor TPar where
    fmap f (Par' a b)  = Par' a (fmap f b)
    fmap f (Seq' a b)  = Seq' a (fmap f b)
    fmap f (Val' x)    = Val' (f x)
    fmap f (Lbl s x)   = Lbl s (fmap f x)

instance A.Applicative TPar where
    pure = Val'
--    f A.<*> x = do {f' <- f; x' <- x; return (f' x')}
--    Dejo esto, asi observamos directamente que pasa.
    (<*>) (Par' l f) x      = Par' l (f A.<*> x)
    (Seq' l f)      <*> x   = Seq' l (f A.<*> x)
    (Lbl (d,v) f)   <*> (Lbl (d',v') x) = Lbl (d++d',v++(' ':v')) (f A.<*> x) -- Por las dudas...
    (Lbl s f)       <*> x = Lbl s (f A.<*> x)
    (Val' f)        <*> x = fmap f x

instance Monad TPar where
    return = A.pure
    (Par' l r)  >>= f = Par' l (r >>= f)
    (Seq' l r)  >>= f = Seq' l (r >>= f)
    (Lbl s x)   >>= f = Lbl s (x >>= f)
    (Val' x)    >>= f = f x

instance Eq a => Eq (TPar a) where
    a == b = ssexec a == ssexec b

instance Ord a => Ord (TPar a) where
    compare a b = compare (ssexec a) (ssexec b)

instance (Num a) => Num (TPar a) where 
    l + r           = app (app (mkVar' "(+)" (+)) l) r
    l * r           = app (app (mkVar' "(*)" (*)) l) r
    abs             = app (mkVar' "abs" abs)
    signum x        = signum A.<$> x
    fromInteger x   = fromInteger A.<$> mkVar x

-- | Reexport <$>. So the user doens't have to import Applicative.
(<$>) :: (a -> b) -> TPar a -> TPar b 
f <$> x = f A.<$> x

-- | Reexport <$>. So the user doens't have to import Applicative.
(<*>) :: TPar (a -> b) -> TPar a -> TPar b 
f <*> x = f A.<*> x

dlbl :: String -> TPar a -> TPar a
dlbl s (Lbl (d,v) x) = Lbl (s++d,v) x
dlbl s x = Lbl (s,"") x

vlbl :: String -> TPar a -> TPar a
vlbl s (Lbl (d,v) x) = Lbl (d,s++(' ':v)) x
vlbl s x = Lbl ("",s) x

-- | Create a label for a par node.
pars :: String -> TPar a -> TPar b -> TPar b
pars s a b = dlbl s $ Par' a b

-- | Create a label for a pseq node.
seqs :: String -> TPar a -> TPar b -> TPar b
seqs s a b = dlbl s $ Seq' a b

infixr 0 `par`, `pseq`
-- | Basic primitive par.
par :: TPar a -> TPar b -> TPar b
par = Par' 

-- | Basic primitive pseq.
pseq :: TPar a -> TPar b -> TPar b
pseq = Seq'

mkVar :: a -> TPar a
mkVar = Val' 

--mkVarHT :: (Lift a) => a -> TPar a
mkVarHT x = do
    newname <- runQ x 
    return (mkVar' (show newname) x)

mkVarHT' x = do
    newname <- runQ [|x|] 
    return (mkVar' (show newname) x)

-- | Create a label for a value.
mkVar' :: String -> a -> TPar a
mkVar' s x = vlbl s $ Val' x

-- | Create a label for a value with show.
mkVars :: (Show a) => a -> TPar a
mkVars x = vlbl (show x) $ Val' x

-- | Create a label for an application.
smap ::String -> (a -> b) -> TPar a -> TPar b
smap s f = app (mkVar' s f)

app :: TPar (a -> b) -> TPar a -> TPar b
app f x = f A.<*> x

--realapp :: TPar (a -> b) -> a -> TPar b
--realapp f x = fmap (\f' -> f' x) f
--
--motherapp :: TPar (a -> b) -> TPar a -> TPar (TPar b)
--motherapp f = fmap (realapp f)

-- | Extract the behaviour from a TPar construction.
exec :: TPar a -> a
exec (Par' l r)  = P.par (exec l) (exec r)
exec (Seq' l r)  = P.pseq (exec l) (exec r)
exec (Lbl _ x)   = exec x
exec (Val' x)    = x 

-- | Drop all the information gathered.
ssexec :: TPar a -> a
ssexec (Par' _ r)   = ssexec r
ssexec (Seq' _ r)   = ssexec r
ssexec (Lbl _ x)    = ssexec x
ssexec (Val' x)     = x 

