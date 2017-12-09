import Prelude hiding (lookup)

data BinaryTree k v = Leaf | Branch k v (BinaryTree k v) (BinaryTree k v) deriving (Eq, Show)

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup _ Leaf = Nothing
lookup key (Branch k v l r) | key == k  = Just v
							| key > k   = lookup key r
							| otherwise = lookup key l

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert key value Leaf = Branch key value Leaf Leaf
insert key value (Branch k v l r) | key == k  = Branch key value l r
								  | key > k   = Branch k v l (insert key value r)
							      | otherwise = Branch k v (insert key value l) r

merge :: BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge b Leaf = b
merge b (Branch k v l r) = Branch k v (merge b l) r

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete _ Leaf = Leaf
delete key (Branch k v r l) | key == k  = merge l r
						    | key > k   = Branch k v l (delete key r)
							| otherwise = Branch k v (delete key l) r
							

