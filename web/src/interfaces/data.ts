export interface Ingredient { id: string; amount: number }
export interface Product {
  name: string
  table: string
  amount: number
  recipe: Ingredient[]
}

export type Data = { items: string[]; products: Product[] }
