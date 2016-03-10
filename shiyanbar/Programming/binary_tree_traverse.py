#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
'''
url: http://www.shiyanbar.com/ctf/1868
题目描述: 给出二叉树的前序遍历序列和中序遍历序列分别是：DBACEGF和ABCDEFG，需要编写程序通过这两组数据求出该树的后
序遍历序列。key格式为：CTF{}
参考文章: http://blog.csdn.net/bone_ace/article/details/46718683
http://www.webtag123.com/python/43481.html
http://www.jb51.net/article/49471.htm
虽然找到了一个二叉树的库(BTrees),但是没有这种低级的根据前序遍历和中序遍历创建树的代码,所以最后还是自己写了


参考数据结构的 C 实现代码:
前序遍历算法
//二叉树的前序遍历递归算法
void PreOrderTraverse( BiTree T )
{
    if ( T == NULL )
        return ;
    printf( "%c",T->data );	//显示结点数据，可以更改为其他对结点操作
    PreOrderTraverse( T->lchild );	//再先序遍历左子树
    PreOrderTraverse( T->rchild );	//最后先序遍历右子树
}

中序遍历算法

//二叉树的中序遍历递归算法
void InorderTraverse( BiTree T )
{
    if ( T == NULL )
        return ;
    InOrderTraverse( T->lchild );	//中序遍历左子树
    printf( "%c",T->data );	//显示结点数据，可以更改为其他对结点操作
    InOrderTraverse( T->rchild );	//最后中序遍历右子树
}

后序遍历算法

//二叉树的后序遍历递归算法
void PostOrderTraverse( BiTree T )
{
    if ( T == NULL )
        return ;
    PostOrderTraverse( T->lchild );	//先后序遍历左子树
    PostOrderTraverse( T->rchild );	//再后序遍历右子树
    printf( "%c",T->data );	//显示结点数据，可以更改为其他对结点操作
}

//按前序输入二叉树中结点的值（一个字符）
//#表示空树，构造二叉链表表示二叉树T
void CreateBiTree( BiTree * T )
{
    TElemType ch;
    scanf( "%c",&ch );
    if ( ch == '#' )
        *T = NULL;
    else
    {
        *T = ( BiTree )malloc( sizeof( BiTNode ) );
        if ( !*T )	exit( OVERFLOW );
        ( *T )->data = ch;	//生成根结点
        CreateBiTree( &( *T )->lchild );	//构造左子树
        CreateBiTree( &( *T )->rchild );	//构造右子树
    }
}
由先序、中序序列构造二叉树的算法：
BiTree createBiTreeByInOrderAndPreOrder( int pre_start,int pre_end,int in_start,int in_end ){
    BiTree root = new BiTNode;
    root->data = preOrder[pre_start];
    root->lchild = root->rchild = NULL;

    for ( int i = in_start ; inOrder[i] != root->data ; ++i ){
        continue;
    }

    int leftLength = i - in_start;
    int rightLength = in_end - i;

    if ( leftLength != 0 ){
        BiTree leftRoot = createBiTreeByInOrderAndPreOrder( pre_start + 1,pre_start + leftLength,in_start,in_start + leftLength - 1 );
        root->lchild = leftRoot;
    }
    if ( rightLength != 0 ){
        BiTree rightRoot = createBiTreeByInOrderAndPreOrder( pre_end - rightLength + 1,pre_end,in_end - rightLength + 1,in_end );
        root->rchild = rightRoot;
    }

    return root;
}

∮已知前序遍历序列和中序遍历序列，可以唯一确定一棵二叉树
∮已知后续遍历序列和中序遍历序列，可以唯一确定一棵二叉树
'''
__author__ = '__L1n__w@tch'

preOrder = list()
inOrder = list()


class BiTNode:
    def __int__(self, data=None, lchild=None, rchild=None):
        self.data = data
        self.lchild = lchild
        self.rchild = rchild


def createBiTreeByInOrderAndPreOrder(pre_start, pre_end, in_start, in_end):
    root = BiTNode()
    root.data = preOrder[pre_start]

    i = inOrder.index(root.data)
    leftLength = i - in_start
    rightLength = in_end - i

    if (leftLength != 0):
        leftRoot = createBiTreeByInOrderAndPreOrder(pre_start + 1, pre_start + leftLength, in_start,
                                                    in_start + leftLength - 1)
        root.lchild = leftRoot
    if (rightLength != 0):
        rightRoot = createBiTreeByInOrderAndPreOrder(pre_end - rightLength + 1, pre_end, in_end - rightLength + 1,
                                                     in_end)
        root.rchild = rightRoot

    return root


def main():
    global preOrder,inOrder
    preOrder = list("DBACEGF")
    inOrder = list("ABCDEFG")
    btree = createBiTreeByInOrderAndPreOrder(0, len(preOrder) - 1, 0, len(inOrder) - 1)
    print(btree.data)


if __name__ == "__main__":
    main()
