import PostData from "@/components/post/post-data"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Textarea } from "@/components/ui/textarea"
import { Separator } from "@/components/ui/separator"
import { Mic, Paperclip } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function IndexPage() {
  return (
    <div className="flex w-full flex-row justify-around px-4">
      <aside className="sticky left-0 top-20 h-screen w-72">
        <h2>Following</h2>
        <ul>
          <li><a href="#">My Friend</a></li>
          <li><a href="#">My Other Friend</a></li>
          <li><a href="#">My Best Friend</a></li>
        </ul>
      </aside>
      <Separator className="h-full" orientation="vertical" />
      <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
        <Card className="flex w-[550px] flex-col gap-y-4 p-2" id="create-post">
          <Avatar>
            <AvatarImage src="https://github.com/shadcn.png" alt="@shadcn" />
            <AvatarFallback>CN</AvatarFallback>
          </Avatar>
          <div>
            <Textarea className="max-h-44" placeholder="Write whats on your mind!" />
            <div className="mt-2 flex items-center justify-between">
              <div>
                <Button variant={null} size="icon">
                  <Paperclip className="h-5 w-5" />
                </Button>
                <Button variant={null} size="icon">
                  <Mic className="h-5 w-5" />
                </Button>
              </div>
              <Button className="px-6">Post</Button>
            </div>
          </div>
        </Card>
        <PostData />
        <PostData />
        <PostData />
        <PostData />
        <PostData />
        <PostData />
        <PostData />
        <PostData />
        <PostData />
      </section>
      <Separator className="h-full" orientation="vertical" />
      <aside className="sticky left-0 top-20 h-screen">
        <h2>Blogroll</h2>
        <ul>
          <li><a href="#">My Friend</a></li>
          <li><a href="#">My Other Friend</a></li>
          <li><a href="#">My Best Friend</a></li>
        </ul>
      </aside>
    </div>
  )
}